Unofficial Pushed.co API wrapper
================================

Overview
---------

Python wrapper for the pushed.co API. https://pushed.co

Send push notifications to mobile devices without writing your own mobile
app. Have notifications pushed to you rather than relying on polling RSS feeds
and the like.


Usage
-----

Currently only the push functionality and some of the OAuth2 is implemented
here.

Basic usage
::
    import pushed

    APP_KEY = 'MY_PUSHED_APP_KEY'
    APP_SECRET = 'MY_PUSHED_APP_SECRET'
    CHANNEL_ALIAS = 'MY_CHANNEL_ALIAS'
    PUSHED_ID = 'PUSHED_ID_FOR_SUBSCRIBER'

    p = pushed.Pushed(APP_KEY, APP_SECRET)

    # Push message to your application's subscribers
    shipment = p.push_app('test app push')

    # Push message to your channel's subscribers
    shipment = p.push_channel('test channel push', CHANNEL_ALIAS)

    # Push message to a user by Pushed ID
    shipment = p.push_pushed_id('test Pushed ID push', PUSHED_ID)

Pushing to a user requires an OAuth2 access token. You must swap a temporary
code for this access token using the Pushed API. These temporary codes arrive
by webhook, when a subscriber follows your authorization link and agrees to the
access.

To generate an authorization link to share with your users
::
    p = pushed.Pushed(APP_KEY, APP_SECRET)
    uri = p.authorization_link('https://example.org/my-webhook-handler')

Using a code to get an access token, then sending a message to the user
::
    p = pushed.Pushed(APP_KEY, APP_SECRET)
    access_token = p.access_token(temporary_code)
    shipment = p.push_user('test user push', access_token)

All 4 push methods return an alphanumeric Shipment ID which you can check
against your Pushed.co control panel. If the Pushed API returns a JSON failure
message then a PushedAPIError will be raised using its type and message fields.

Installation
------------

Using pip ::
::
    pip install pushed

