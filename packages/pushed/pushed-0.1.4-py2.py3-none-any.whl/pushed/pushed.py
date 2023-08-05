# encoding: utf-8

import json
import requests

BASE_URL = 'https://api.pushed.co'
API_VERSION = '1'
PUSH = 'push'
OAUTH = 'oauth'
ACCESS_TOKEN = 'oauth/access_token'
USER_AGENT = 'python-pushed/0.1.4'


class Pushed(object):
    '''Pushed.co API client class.

    Param: app_key -> A Pushed.co application key
           app_secret -> The secret authorizing the application key
    '''

    def __init__(self, app_key, app_secret):
        self.app_key, self.app_secret = app_key, app_secret

    def push_app(self, content, content_url=None):
        '''Push a notification to a Pushed application.
        
        Param: content -> content of Pushed notification message
               content_url (optional) -> enrich message with URL
        Returns Shipment ID as string
        '''
        parameters = {
            'app_key': self.app_key,
            'app_secret': self.app_secret
        }
        return self._push(content, 'app', parameters, content_url)

    def push_channel(self, content, channel, content_url=None):
        '''Push a notification to a Pushed channel.

        Param: content -> content of Pushed notification message
               channel -> string identifying a Pushed channel
               content_url (optional) -> enrich message with URL
        Returns Shipment ID as string
        '''
        parameters = {
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'target_alias': channel
        }
        return self._push(content, 'channel', parameters, content_url)

    def push_user(self, content, access_token, content_url=None):
        '''Push a notification to a specific pushed user.

        Param: content -> content of Pushed notification message
               access_token -> OAuth access token
               content_url (optional) -> enrich message with URL
        Returns Shipment ID as string
        '''
        parameters = {
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'access_token': access_token
        }
        return self._push(content, 'user', parameters, content_url)

    def push_pushed_id(self, content, pushed_id, content_url=None):
        '''Push a notification to a specific pushed user by Pushed ID.

        Param: content -> content of Pushed notification message
               pushed_id -> user's pushed ID
               content_url (optional) -> enrich message with URL
        Returns Shipment ID as string
        '''
        parameters = {
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'pushed_id': pushed_id,
            'target_alias': 'Nothing'   # Required, but seems unused
        }
        return self._push(content, 'pushed_id', parameters, content_url)

    def _push(self, content, target_type, parameters={}, content_url=None):
        parameters.update(
            {
                'content': content,
                'target_type': target_type
            }
        )
        if content_url is not None:
            parameters.update(
                {
                    'content_type': 'url',
                    'content_extra': content_url
                }
            )
        push_uri = "/".join([BASE_URL, API_VERSION, PUSH])
        success, response = self._request(push_uri, parameters)
        if success:
            return response['response']['data']['shipment']
        else:
            raise PushedAPIError(
                response['error']['type'],
                response['error']['message']
            )

    def access_token(self, code):
        '''Exchange a temporary OAuth2 code for an access token.

        Param: code -> temporary OAuth2 code from a Pushed callback
        Returns access token as string
        '''
        parameters = {"code": code}
        access_uri = "/".join([BASE_URL, API_VERSION, ACCESS_TOKEN])
        # RFC non-compliant response prevents use of standard OAuth modules
        success, response = self._request(access_uri, parameters)
        if success:
            return response['response']['data']['access_token']
        else:
            raise PushedAPIError(
                response['error']['type'],
                response['error']['message']
            )

    def _request(self, url, parameters):
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': USER_AGENT
        }
        r = requests.post(url, data=json.dumps(parameters), headers=headers)
        return (
            str(r.status_code).startswith('2'),
            r.json()
        )

    def authorization_link(self, redirect_uri):
        '''Construct OAuth2 authorization link.

        Params:    redirect_uri -> URI for receiving callback with token
        Returns authorization URL as string
        '''
        args = '?client_id=%s&redirect_uri=%s' % (
            self.app_key,
            redirect_uri
        )
        uri = "/".join([BASE_URL, API_VERSION, OAUTH, args])
        return uri

class PushedAPIError(Exception):
    '''Raise when an API request does not return a success status'''

