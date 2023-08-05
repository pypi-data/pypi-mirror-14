# encoding: utf-8

"""
test_pushed
------------------------------

Tests for 'pushed' module
"""

import unittest
import pushed

from mock import mock, patch

PUSHSUCCESS = {
    'response': {
        'type': 'shipment_successfully_queued',
        'message': 'Shipment successfully queued.',
        'data': {
            'shipment': '01234ABCDE'
        }
    }
}
PUSHFAIL = {
    'error': {
        'message': 'App credentials are not valid.',
        'type': 'app_credentials_are_not_valid'
    }
}
TOKENSUCCESS = {
    'response': {
        'data': {
            'access_token': 'LONG_ACCESS_TOKEN'
        },
        'message': 'App has been granted access.',
        'type': 'app_authorization_accepted'
    }
}
TOKENFAIL = {
    'error': {
        'message': 'Code is invalid.',
        'type': 'invalid_code'
    }
}


class TestPushed(unittest.TestCase):

    def setUp(self):
        self.pushed = pushed.Pushed("APP_KEY", "APP_SECRET")
        pass

    def test_authorization_link(self):
        self.assertEqual(
            self.pushed.authorization_link('https://example.org/test'),
            (
                'https://api.pushed.co/1/oauth/?'
                'client_id=APP_KEY'
                '&redirect_uri=https://example.org/test'
            )
        )

    @mock.patch('pushed.Pushed._request', return_value=(True, TOKENSUCCESS))
    def test_access_token(self, m_request):
        self.assertEqual(self.pushed.access_token(12345), 'LONG_ACCESS_TOKEN')

    @mock.patch('pushed.Pushed._request', return_value=(False, TOKENFAIL))
    def test_access_token_fail(self, m_request):
        self.assertRaises(
            pushed.pushed.PushedAPIError,
            self.pushed.access_token,
            12345
        )

    @mock.patch('pushed.Pushed._request', return_value=(True, PUSHSUCCESS))
    def test_push_app(self, m_request):
        shipment = self.pushed.push_app('app push')
        args, kwargs = m_request.call_args_list[0]
        self.assertEqual(args[1], {
                'content': 'app push', 'app_secret': 'APP_SECRET',
                'target_type': 'app', 'app_key': 'APP_KEY'
            }
        )
        self.assertEqual(shipment, '01234ABCDE')

    @mock.patch('pushed.Pushed._request', return_value=(True, PUSHSUCCESS))
    def test_push_app_url(self, m_request):
        shipment = self.pushed.push_app(
            'app push',
            content_url='http://example.com'
        )
        args, kwargs = m_request.call_args_list[0]
        self.assertEqual(args[1], {
                'content': 'app push', 'app_secret': 'APP_SECRET',
                'target_type': 'app', 'app_key': 'APP_KEY',
                'content_type': 'url', 'content_extra': 'http://example.com'
            }
        )
        self.assertEqual(shipment, '01234ABCDE')

    @mock.patch('pushed.Pushed._request', return_value=(False, PUSHFAIL))
    def test_push_app_fail(self, m_request):
        self.assertRaises(
            pushed.pushed.PushedAPIError,
            self.pushed.push_app,
            'app push'
        )

    @mock.patch('pushed.Pushed._request', return_value=(True, PUSHSUCCESS))
    def test_push_channel(self, m_request):
        shipment = self.pushed.push_channel('channel push', 'CHANNEL')
        args, kwargs = m_request.call_args_list[0]
        self.assertEqual(args[1], {
                'content': 'channel push', 'app_secret': 'APP_SECRET',
                'target_type': 'channel', 'app_key': 'APP_KEY',
                'target_alias': 'CHANNEL',
            }
        )
        self.assertEqual(shipment, '01234ABCDE')

    @mock.patch('pushed.Pushed._request', return_value=(True, PUSHSUCCESS))
    def test_push_channel_url(self, m_request):
        shipment = self.pushed.push_channel(
            'channel push',
            'CHANNEL', 
            content_url='http://example.com'
        )
        args, kwargs = m_request.call_args_list[0]
        self.assertEqual(args[1], {
                'content': 'channel push', 'app_secret': 'APP_SECRET',
                'target_type': 'channel', 'app_key': 'APP_KEY',
                'target_alias': 'CHANNEL', 'content_type': 'url',
                'content_extra': 'http://example.com'
            }
        )
        self.assertEqual(shipment, '01234ABCDE')

    @mock.patch('pushed.Pushed._request', return_value=(True, PUSHSUCCESS))
    def test_push_user(self, m_request):
        shipment = self.pushed.push_user('user push', 'ACCESS_TOKEN')
        args, kwargs = m_request.call_args_list[0]
        self.assertEqual(args[1], {
                'content': 'user push', 'app_secret': 'APP_SECRET',
                'target_type': 'user', 'app_key': 'APP_KEY',
                'access_token': 'ACCESS_TOKEN',
            }
        )
        self.assertEqual(shipment, '01234ABCDE')

    @mock.patch('pushed.Pushed._request', return_value=(True, PUSHSUCCESS))
    def test_push_user_url(self, m_request):
        shipment = self.pushed.push_user(
            'user push',
            'ACCESS_TOKEN',
            content_url='http://example.com'
        )
        args, kwargs = m_request.call_args_list[0]
        self.assertEqual(args[1], {
                'content': 'user push', 'app_secret': 'APP_SECRET',
                'target_type': 'user', 'app_key': 'APP_KEY',
                'access_token': 'ACCESS_TOKEN', 'content_type': 'url',
                'content_extra': 'http://example.com'
            }
        )
        self.assertEqual(shipment, '01234ABCDE')
		
    @mock.patch('pushed.Pushed._request', return_value=(True, PUSHSUCCESS))
    def test_push_pushedid(self, m_request):
        shipment = self.pushed.push_pushed_id('pushedid push', 'PUSHED_ID')
        args, kwargs = m_request.call_args_list[0]
        self.assertEqual(args[1], {
                'content': 'pushedid push', 'app_secret': 'APP_SECRET',
                'target_type': 'pushed_id', 'app_key': 'APP_KEY',
                'target_alias': 'Nothing', 'pushed_id': 'PUSHED_ID'
            }
        )
        self.assertEqual(shipment, '01234ABCDE')

    @mock.patch('pushed.Pushed._request', return_value=(True, PUSHSUCCESS))
    def test_push_pushedid_url(self, m_request):
        shipment = self.pushed.push_pushed_id(
            'pushedid push',
            'PUSHED_ID', 
            content_url='http://example.com'
        )
        args, kwargs = m_request.call_args_list[0]
        self.assertEqual(args[1], {
                'content': 'pushedid push', 'app_secret': 'APP_SECRET',
                'target_type': 'pushed_id', 'app_key': 'APP_KEY',
                'target_alias': 'Nothing', 'pushed_id': 'PUSHED_ID',
                'content_type': 'url',
                'content_extra': 'http://example.com'
            }
        )
        self.assertEqual(shipment, '01234ABCDE')
		

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()

