from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import daemon
try:
	from daemon.pidlockfile import PIDLockFile
except ImportError:
	from daemon.pidfile import PIDLockFile

import logging
import optparse
import os
import pwd
import signal
import struct
from SocketServer import ThreadingTCPServer
from socket import AF_UNIX, SOL_SOCKET
import sys
import threading
import urlparse
from vesna.alh import ALHException, ALHWeb

SO_PEERCRED = 17

log = logging.getLogger(__name__)

class BaseAuthenticator(object):
	def is_allowed(self, cluster_uid, pid, uid, gid):
		return True

class NullAuthenticator(BaseAuthenticator):
	pass

class StaticAuthenticator(BaseAuthenticator):
	def __init__(self, clusters, getpwnam=pwd.getpwnam):
		self.cluster_uid_to_user_id_set = {}
		for cluster_uid, config in clusters.items():
			names = config.get('user')
			if names is None:
				continue
			if isinstance(names, str):
				names = (names,)

			self.cluster_uid_to_user_id_set[cluster_uid] = user_id_set = set()

			for name in names:
				try:
					user_id = getpwnam(name).pw_uid
				except KeyError:
					log.error("Unknown user '%s' in config for cluster '%s' - ignoring" % (
							name, cluster_uid))
				else:
					user_id_set.add(user_id)

	def is_configured(self):
		return bool(self.cluster_uid_to_user_id_set)

	def is_allowed(self, cluster_uid, pid, uid, gid):
		allowed_uids = self.cluster_uid_to_user_id_set.get(cluster_uid, ())
		return uid in allowed_uids or uid == 0

class UnixSocketHTTPServer(ThreadingTCPServer):
	allow_reuse_address = 1
	address_family = AF_UNIX

	def server_close(self):
		ThreadingTCPServer.server_close(self)
		os.unlink(self.server_address)

class HTTPRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		parsed_path = urlparse.urlparse(self.path)

		if parsed_path.path == '/communicator':
			self.do_communicator(parsed_path)
		else:
			self.send_error(404, 'path not found')

	def send_err(self, code, msg=''):
		self.send_response(code)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		self.wfile.write("%s\r\n" % (msg,))

	def do_communicator(self, parsed_path):
		query = urlparse.parse_qs(parsed_path.query)

		cluster_uid = query.get('cluster_uid')
		if cluster_uid is None:
			self.send_error(400, 'cluster uid missing')
			return
		cluster_uid = cluster_uid[0]

		alh = self.server.proxy.clusters.get(cluster_uid)

		if alh is None:
			self.send_error(404, 'cluster uid not found')
			return

		if not self.is_authorized(cluster_uid):
			self.send_error(403, 'not authorized')
			return

		self.do_alh_request(query, alh)

	def _split_resource_args(self, resource):

		f = resource.split('?', 1)
		if len(f) == 1:
			return f[0], ""
		else:
			return f[0], f[1]

	def do_alh_request(self, query, alh):

		method = query.get('method')
		if method is None:
			self.send_error(400, 'alh method missing')
			return
		method = method[0].lower()

		resource = query.get('resource')
		if resource is None:
			self.send_error(400, 'alh resource missing')
			return
		resource, args = self._split_resource_args(resource[0])

		if method == 'get':
			try:
				resp = alh.get(resource, args)
			except ALHException, e:
				resp = str(e)
		elif method == 'post':
			content = query.get('content')
			if content is None:
				self.send_error(400, 'alh content missing')
				return
			data = content[0]
			try:
				resp = alh.post(resource, data, args)
			except ALHException, e:
				resp = str(e)
		else:
			self.send_error(400, "invalid alh method")
			return

		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		self.wfile.write(resp)

	def is_authorized(self, cluster_uid):
		creds = self.request.getsockopt(SOL_SOCKET, SO_PEERCRED, struct.calcsize('3i'))
		pid, uid, gid = struct.unpack('3i', creds)

		log.info('pid: %d, uid: %d, gid %d' % (pid, uid, gid))

		return self.server.proxy.auth.is_allowed(cluster_uid, pid, uid, gid)

	def log_message(self, format, *args):
		log.info(format % args)

class ALHAuthProxy(object):
	def __init__(self, socket_path, auth=None, clusters={}):
		self.socket_path = socket_path
		self.clusters = clusters

		if auth is None:
			self.auth = NullAuthenticator()
		else:
			self.auth = auth

	def start(self):
		log.info("Starting HTTP server")
		self.httpd = UnixSocketHTTPServer(self.socket_path, HTTPRequestHandler)
		self.httpd.proxy = self
		self.httpd.serve_forever()

	def stop(self):
		self.httpd.shutdown()
		self.httpd.server_close()
		del self.httpd

DEFAULT_CONFIG = "/etc/vesna_alh_auth_proxy.conf"

def load_config(path=DEFAULT_CONFIG):
	config = {}
	execfile(path, {}, config)
	return config

def create_clusters(config):

	clusters = {}

	for uid, desc in config.items():
		clusters[uid] = ALHWeb(desc['base_url'], desc['cluster_id'])

	return clusters

def main():
	parser = optparse.OptionParser('%prog [options]',
	        description="ALH authorization proxy for OMF")
	parser.add_option('-c', '--config', metavar='FILE', dest='config', default=DEFAULT_CONFIG,
	        help='Use FILE for configuration')

	options, args = parser.parse_args()

	config = load_config(options.config)

	logging.basicConfig(
			filename=config['log_file'],
			level=logging.DEBUG,
			format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
			)
	log.info("Forking into background")

	clusters = create_clusters(config['clusters'])

	auth = StaticAuthenticator(config['clusters'])
	if not auth.is_configured():
		log.warning("StaticAuthenticator not configured. Falling back to NullAuthenticator")
		auth = NullAuthenticator()

	proxy = ALHAuthProxy(config['socket'], auth=auth, clusters=clusters)

	def stop(signal, frame):
		log.info("Caught signal")
		proxy.stop()

	with daemon.DaemonContext(
			signal_map={
				signal.SIGINT: stop,
				signal.SIGTERM: stop
			},
			files_preserve=[logging.root.handlers[0].stream],
			pidfile=PIDLockFile(config['pid_file'])):

		try:
			thread = threading.Thread(target=proxy.start)
			thread.start()

			while thread.isAlive():
				thread.join(timeout=1.)
		except:
			log.exception("Unhandled exception")

		log.info("Stopped")

if __name__ == "__main__":
	main()
