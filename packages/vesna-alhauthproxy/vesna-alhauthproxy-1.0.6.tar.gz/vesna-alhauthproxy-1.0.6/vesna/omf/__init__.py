import logging
import os
import requests_unixsocket
import time
import urllib
from vesna.alh import ALHProtocol, ALHException, TerminalError
from vesna.omf.proxy import load_config

log = logging.getLogger(__name__)

class ALH(ALHProtocol):
	"""ALH protocol implementation for access through the OMF framework.

	This class is typically used to access the coordinator when accessing
	the tesbed through the OMF framework. No parameters are usually needed
	for the constructor. The appropriate values are discovered
	automatically through OMF.
	"""
	def __init__(self, cluster_uid=None, socket_path=None):
		self.cluster_uid = os.environ.get('CLUSTER_UID', cluster_uid)
		if self.cluster_uid is None:
			raise ALHException("CLUSTER_UID undefined. This script should be ran by "
					"the OMF experiment controller")

		if socket_path is None:
			socket_path = load_config()['socket']

		self.base_url = 'http+unix://%s/communicator' % (urllib.quote(socket_path, safe=''),)

	def _send(self, params):
		session = requests_unixsocket.Session()
		resp = session.get(self.base_url, params=params)

		# Raise an exception if we got anything else than a 200 OK
		if resp.status_code != 200:
			raise TerminalError(resp.text)

		return resp.content

	def _send_with_error(self, params):
		# loop until communication channel is free and our request
		# goes through.
		time_start = time.time()
		while True:
			resp = self._send(params)
			if resp != "ERROR: Communication in progress":
				break

			log.info("communicator is busy (have been waiting for %d s)" %
					(time.time() - time_start))

			time.sleep(1)

		self._check_for_sneaky_error(resp)

		self._log_response(resp)
		return resp

	def _get(self, resource, *args):
		self._log_request("GET", resource, args)

		arg = "".join(args)
		params = {
				'method': 'get',
				'resource': '%s?%s' % (resource, arg),
				'cluster_uid': self.cluster_uid,
		}

		return self._send_with_retry(params)

	def _post(self, resource, data, *args):
		self._log_request("POST", resource, args, data)

		arg = "".join(args)
		params = {
				'method': 'post',
				'resource': '%s?%s' % (resource, arg),
				'content': data,
				'cluster_uid': self.cluster_uid,
		}

		return self._send_with_retry(params)
