from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import logging
import requests_unixsocket
import threading
import unittest
import os

from vesna.omf.proxy import ALHAuthProxy
from vesna.alh import ALHWeb

logging.basicConfig(level=logging.WARNING)

class MockALH(object):
	def __init__(self):
		self.requests = []

	def get(self, resource, *args):
		self.requests.append(('get', resource, args))
		return 'get'

	def post(self, resource, data, *args):
		self.requests.append(('post', resource, data, args))
		return 'post'

class TestAuthProxyMockedALH(unittest.TestCase):

	def setUp(self):
		self.socket_path = "/tmp/alh.sock"
		self.a = None

	def tearDown(self):
		if self.a is not None:
			self.a.stop()
			self.t.join()

	def _start(self, **kwargs):
		self.alh = MockALH()

		if 'clusters' not in kwargs:
			kwargs['clusters'] = clusters = {'test': self.alh}

		self.a = ALHAuthProxy(self.socket_path, **kwargs)
		self.t = threading.Thread(target=self.a.start)
		self.t.start()

		while not os.path.exists(self.socket_path):
			pass

	def _get(self, path, params=None):
		session = requests_unixsocket.Session()
		url = 'http+unix://%s/%s' % (self.socket_path.replace('/', '%2F'), path)
		return session.get(url, params=params)

	def test_invalid_url(self):
		self._start()

		r = self._get('foo')
		self.assertEqual(r.status_code, 404)

	def test_missing_uid(self):
		self._start()

		r = self._get('communicator')
		self.assertEqual(r.status_code, 400)

	def test_wrong_uid(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'foo'})
		self.assertEqual(r.status_code, 404)

	def test_no_method(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test'})
		self.assertEqual(r.status_code, 400)

	def test_wrong_method(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'foo'})
		self.assertEqual(r.status_code, 400)

	def test_get_no_resource(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'get'})
		self.assertEqual(r.status_code, 400)

	def test_get(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'get', 'resource':'/test'})
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.text, 'get')
		self.assertEqual(self.alh.requests, [('get', '/test', ('',))])

	def test_post_no_resource(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'post'})
		self.assertEqual(r.status_code, 400)

	def test_post_no_data(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'post', 'resource':'/test'})
		self.assertEqual(r.status_code, 400)

	def test_post(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'post', 'resource':'/test', 'content': 'data'})
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.text, 'post')
		self.assertEqual(self.alh.requests, [('post', '/test', 'data', ('',))])

	def test_auth(self):

		l = []

		class MockAuthenticator:
			def is_allowed(self, cluster_uid, pid, uid, gid):
				l.append((cluster_uid, pid, uid, gid))
				return False

		self._start(auth=MockAuthenticator())

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'get', 'resource':'/test'})
		self.assertEqual(r.status_code, 403)
		self.assertEqual(self.alh.requests, [])
		self.assertEqual(l[0], ('test', os.getpid(), os.getuid(), os.getgid()))

	def test_blocking(self):
		# if one cluster blocks, other clusters should still be able to
		# serve requests

		class BlockingALH(MockALH):
			def __init__(self):
				super(BlockingALH, self).__init__()
				self.lock = threading.Lock()
				self.lock.acquire()

			def get(self, *args):
				self.lock.acquire()
				r = super(BlockingALH, self).get(*args)
				self.lock.release()
				return r

		working_alh = MockALH()
		blocking_alh = BlockingALH()

		clusters = {
			'working': working_alh,
			'blocking': blocking_alh,
		}

		self._start(clusters=clusters)

		def blocking_request():
			r = self._get('communicator',
					{'cluster_uid': 'blocking', 'method': 'get', 'resource': '/test'})
			self.assertEqual(r.status_code, 200)

		blocking_thread = threading.Thread(target=blocking_request)
		blocking_thread.start()

		r = self._get('communicator',
				{'cluster_uid': 'working', 'method': 'get', 'resource': '/test'})
		self.assertEqual(r.status_code, 200)

		blocking_alh.lock.release()
		blocking_thread.join()

	def test_concurrent_request(self):
		# currently we allow multiple concurrent requests to one
		# cluster. It seems nothing should break by that. One request
		# will get "communication in progress" error from the
		# coordinator, but it feels like it's not our place to fix
		# that.

		class BlockingALH(MockALH):
			def __init__(self):
				super(BlockingALH, self).__init__()
				self.lock = threading.Lock()
				self.lock.acquire()
				self.n = 0
				self.maxn = 0

			def get(self, *args):
				self.n += 1
				self.maxn = max(self.n, self.maxn)
				if self.n == 1:
					return self.get1(*args)
				else:
					return self.get2(*args)
				self.n -= 1

			def get1(self, *args):
				self.lock.acquire()
				r = super(BlockingALH, self).get(*args)
				self.lock.release()
				return r

			def get2(self, *args):
				return super(BlockingALH, self).get(*args)

		alh = BlockingALH()

		clusters = {
			'test': alh,
		}

		self._start(clusters=clusters)

		def blocking_request():
			r = self._get('communicator',
					{'cluster_uid': 'test', 'method': 'get', 'resource': '/test'})
			self.assertEqual(r.status_code, 200)

		t1 = threading.Thread(target=blocking_request)
		t1.start()

		t2 = threading.Thread(target=blocking_request)
		t2.start()
		t2.join()

		alh.lock.release()

		t1.join()

		self.assertEqual(alh.maxn, 2)

class TestAuthProxyALHWeb(unittest.TestCase):

	def setUp(self):
		self.path = "/tmp/alh.sock"
		self.a = None

		self.l = l = [0]

		class MockHTTPRequestHandler(BaseHTTPRequestHandler):
			def do_GET(self):
				self.send_response(200)
				self.end_headers()

				self.wfile.write('bar')

				l[0] += 1

			def log_message(self, format, *args):
				pass

		server_address = ('localhost', 12345)
		self.httpd = HTTPServer(server_address, MockHTTPRequestHandler)
		self.t = threading.Thread(target=self.httpd.serve_forever)
		self.t.start()

	def tearDown(self):
		self.httpd.shutdown()
		self.t.join()

		if self.a is not None:
			self.a.stop()
			self.t2.join()

	def _start(self, **kwargs):
		self.alh = ALHWeb("http://localhost:12345", "1")
		clusters = {'test': self.alh}

		self.a = ALHAuthProxy(self.path, clusters=clusters, **kwargs)
		self.t2 = threading.Thread(target=self.a.start)
		self.t2.start()

		while not os.path.exists(self.path):
			pass

	def _get(self, path, params=None):
		session = requests_unixsocket.Session()
		return session.get('http+unix://%s/%s' % (self.path.replace('/', '%2F'), path), params=params)


	def test_proxy(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'get', 'resource':'/test'})
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.text, 'bar')
		self.assertEqual(self.l[0], 1)

from vesna.omf import ALH

class TestOMFALH(unittest.TestCase):
	def setUp(self):
		self.socket_path = "/tmp/alh.sock"

		self.alh = MockALH()

		clusters = {'test': self.alh}

		self.a = ALHAuthProxy(self.socket_path, clusters=clusters)
		self.t = threading.Thread(target=self.a.start)
		self.t.start()

		while not os.path.exists(self.socket_path):
			pass

	def tearDown(self):
		if self.a is not None:
			self.a.stop()
			self.t.join()

	def test_get_request(self):
		alh = ALH(cluster_uid='test', socket_path=self.socket_path)
		r = alh.get('hello')

		self.assertEqual(r, 'get')

	def test_post_request(self):
		alh = ALH(cluster_uid='test', socket_path=self.socket_path)
		r = alh.post('hello', '1')

		self.assertEqual(r, 'post')

from vesna.omf.proxy import StaticAuthenticator

class MockStructPasswd: pass

def mock_getpwnam(name):
	assert name.startswith("user")

	s = MockStructPasswd()
	s.pw_uid = int(name[4:])
	return s

class TestStaticAuthenticator(unittest.TestCase):
	def test_no_config(self):
		clusters = {
			"cluster1": {
				"cluster_id": 1
			},
			"cluster2": {
				"cluster_id": 2
			},
		}

		a = StaticAuthenticator(clusters)
		self.assertFalse(a.is_configured())

	def test_with_config(self):
		clusters = {
			"cluster1": {
				"cluster_id": 1,
				"user": "user1"
			},
			"cluster2": {
				"cluster_id": 2,
				"user": "user2"
			},
		}

		a = StaticAuthenticator(clusters, getpwnam=mock_getpwnam)
		self.assertTrue(a.is_configured())

		self.assertTrue(a.is_allowed("cluster1", 0, 1, 1))
		self.assertFalse(a.is_allowed("cluster1", 0, 2, 1))
		self.assertTrue(a.is_allowed("cluster2", 0, 2, 1))

		# always allow root
		self.assertTrue(a.is_allowed("cluster1", 0, 0, 1))
		self.assertTrue(a.is_allowed("cluster2", 0, 0, 1))

	def test_with_config_list(self):
		clusters = {
			"cluster1": {
				"cluster_id": 1,
				"user": [ "user1", "user3" ]
			},
			"cluster2": {
				"cluster_id": 2,
				"user": "user2"
			},
		}

		a = StaticAuthenticator(clusters, getpwnam=mock_getpwnam)
		self.assertTrue(a.is_configured())

		self.assertTrue(a.is_allowed("cluster1", 0, 1, 1))
		self.assertFalse(a.is_allowed("cluster1", 0, 2, 1))
		self.assertTrue(a.is_allowed("cluster1", 0, 3, 1))

if __name__ == '__main__':
	unittest.main()
