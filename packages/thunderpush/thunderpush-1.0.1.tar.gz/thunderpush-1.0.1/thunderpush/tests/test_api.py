try:
    import simplejson as json
except ImportError:
    import json

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from thunderpush.api import urls
from thunderpush.sortingstation import SortingStation
from thunderpush.tests.mocks import DummyThunderSocketHandler

API_PUBLIC = 'foo'
API_SECRET = 'bar'


class APITestCase(AsyncHTTPTestCase):
    def get_app(self):
        self.app = Application(urls)
        return self.app

    def setUp(self):
        super(APITestCase, self).setUp()
        self.user1 = DummyThunderSocketHandler()
        self.user2 = DummyThunderSocketHandler()
        self.messenger = SortingStation.instance().create_messenger(
            API_PUBLIC, API_SECRET
        )
        self.messenger.register_user(self.user1)
        self.messenger.register_user(self.user2)
        self.messenger.subscribe_user_to_channel(self.user1, "test1")
        self.messenger.subscribe_user_to_channel(self.user2, "test1")
        self.messenger.subscribe_user_to_channel(self.user1, "test2")

    def tearDown(self):
        super(APITestCase, self).tearDown()
        SortingStation.instance().delete_messenger(self.messenger)

    def call_api(self, method, endpoint, **kwargs):
        return self.fetch(
            '/api/1.0.0/{0}{1}'.format(API_PUBLIC, endpoint),
            method=method,
            headers={
                'X-Thunder-Secret-Key': API_SECRET,
                'Content-Type': 'application/json'
            },
            **kwargs
        )

    def test_send_to_channel(self):
        body = json.dumps({'test': 1})
        response = self.call_api('POST', '/channels/test1/', body=body)
        self.assertEqual(json.loads(response.body)['count'], 2)

    def test_channel_user_list(self):
        response = self.call_api('GET', '/channels/test1/')
        users = json.loads(response.body)['users']
        self.assertTrue(self.user1.userid in users)
        self.assertTrue(self.user2.userid in users)

    def test_user_count(self):
        response = self.call_api('GET', '/users/')
        self.assertEqual(json.loads(response.body)['count'], 2)

    def test_check_if_user_online(self):
        fmt = '/users/{0}/'
        response = self.call_api('GET', fmt.format(self.user1.userid))
        self.assertTrue(json.loads(response.body)['online'])
        response = self.call_api('GET', fmt.format('nonexistentuser'))
        self.assertFalse(json.loads(response.body)['online'])

    def test_send_to_user(self):
        endpoint = '/users/{0}/'.format(self.user1.userid)
        body = json.dumps({'test': 1})
        response = self.call_api('POST', endpoint, body=body)
        self.assertEqual(json.loads(response.body)['count'], 1)

    def test_disconnect_user(self):
        endpoint = '/users/{0}/'.format(API_PUBLIC, self.user1.userid)
        response = self.call_api('DELETE', endpoint)
        self.assertEqual(response.code, 204)
