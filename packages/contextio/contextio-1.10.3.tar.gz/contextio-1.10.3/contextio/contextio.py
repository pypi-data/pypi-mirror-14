from __future__ import absolute_import

import pkg_resources
import logging
import six
from rauth import OAuth1Session
from requests.exceptions import HTTPError

from contextio.lib.v2_0 import helpers
from contextio.lib.v2_0.resources.account import Account
from contextio.lib.v2_0.resources.connect_token import ConnectToken
from contextio.lib.v2_0.resources.discovery import Discovery
from contextio.lib.v2_0.resources.oauth_provider import OauthProvider


class ContextIO(object):

    """Parent class of module. This handles authentication and requests.

    Parameters:
        consumer_key: string - your Context.IO consumer key
        consumer_secret: string - your Context.IO consumer secret
        debug: string - Set to None by default. If you want debug messages,
            set to either 'print' or 'log'. If set to 'print', debug messages
            will be printed out. Useful for python's interactive console. If
            set to 'log' will send debug messages to logging.debug()
    """

    def __init__(self, consumer_key, consumer_secret, debug=None, url_base="https://api.context.io", version="2.0"):
        """Constructor that creates oauth2 consumer and client.

        Required Arguments:
            consumer_key: string - your api key
            consumer_secret: string - you api secret

        Optional Arguments:
            debug: if used, set to either 'print' or 'log' - if print, debug
                messages will be sent to stdout. If set to 'log' will send
                to logging.debug()
        """
        self.version = version
        self.debug = debug
        if self.debug is True:   # for people who don't read the code and just set debug=True
            self.debug = "print"
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.url_base = url_base

        self.session = OAuth1Session(self.consumer_key, self.consumer_secret)

    def _debug(self, response):
        """Prints or logs a debug message.

        Required Arguments:
            response: object - the rauth response object.

        Returns:
            None
        """

        if self.debug:
            message = (
                "--------------------------------------------------\n"
                "URL:    {0}\nMETHOD: {1}\nSTATUS: 2\n\nREQUEST\n{3}\n\n"
                "RESPONSE\n{4}\n").format(
                    response.request.url, response.request.method, response.status_code,
                    response.request.__dict__, response.__dict__)

            if self.debug == "print":
                six.print_(message)
            elif self.debug == "log":
                logging.debug(message)

    def _request_uri(self, uri="", method="GET", params={}, headers={}, body=""):
        """Assembles the request uri and calls the request method.

        Required Arguments:
            uri: string - the assembled API endpoint.

        Optional Parameters:
            method: string - the method of the request. Possible values are
                'GET', 'POST', 'DELETE', 'PUT'
            params: dict - parameters to pass along
            headers: dict - any specific http headers
            body: string - request body, only used on a few PUT statements

        Returns:
            typically, JSON - depends on the API call, refer to the other
                method docstrings for more details.
        """
        url = "/".join((self.url_base, self.version, uri))

        try:
            lib_version = pkg_resources.require("contextio")[0].version
        except:
            lib_version = "dev"

        headers.update(
            {"user-agent": "contextio/{0}/python-lib-{1}".format(self.version, lib_version)})

        if method == "POST":
            params['body'] = body
            response = self.session.request(
                method, url, header_auth=True, data=params, headers=headers)
        else:
            response = self.session.request(
                method, url, header_auth=True, params=params, headers=headers, data=body)

        self._debug(response)
        if response.status_code >= 200 and response.status_code < 300:
            try:
                response_body = response.json()
            except UnicodeDecodeError:
                response_body = response.content
            except ValueError:
                response_body = response.text

            return response_body
        else:
            raise HTTPError(response=response)


    def get_accounts(self, **params):
        """List of Accounts.

        GET method for the accounts resource.

        Documentation: http://context.io/docs/2.0/accounts#get

        Optional Arguments:
            email: string - Only return account associated
                to this email address
            status: string - Only return accounts with sources
                whose status is of a specific value. If an account has many
                sources, only those matching the given value will be
                included in the response. Possible statuses are:
                INVALID_CREDENTIALS, CONNECTION_IMPOSSIBLE,
                NO_ACCESS_TO_ALL_MAIL, OK, TEMP_DISABLED and DISABLED
            status_ok: int - Only return accounts with sources
                whose status is of a specific value. If an account has many
                sources, only those matching the given value will be included
                in the response. Possible statuses are: INVALID_CREDENTIALS,
                CONNECTION_IMPOSSIBLE, NO_ACCESS_TO_ALL_MAIL, OK, TEMP_DISABLED
                and DISABLED
            limit: int - The maximum number of results to return
            offset: int - Start the list at this offset (zero-based)

        Returns:
            A list of Account objects
        """
        all_args = ["email", "status", "status_ok", "limit", "offset"]

        params = helpers.sanitize_params(params, all_args)
        return [Account(self, obj) for obj in self._request_uri("accounts", params=params)]

    def post_account(self, **params):
        """Add a new account.

        POST method for the accounts resource.

        You can optionally pass in the params to simultaneously add a source
        with just this one call. In order to accomplish this you must include all of the
        required parameters to create a source AS WELL AS one of the following:
            - the password for the source
            - the provider_refresh_token AND provider_consumer_key

            *see https://context.io/docs/2.0/accounts/sources#post for more information*

        Documentation: http://context.io/docs/2.0/accounts#post

        Required Arguments:
            email: string - The primary email address of the account holder.
            migrate_account_id: string - Existing user_id (from lite) you want
               to migrate to 2.0. Either migrate_account_id or email must be specified

        Optional Arguments:
            first_name: string - First name of the account holder.
            last_name: string - Last name of the account holder.

        If adding a source in the same call:
        Required Arguments:
            server: string - Name or IP of the IMAP server, eg. imap.gmail.com
            username: string - The username used to authenticate an IMAP
                connection. On some servers, this is the same thing as
                the primary email address.
            use_ssl: integer - Set to 1 if you want SSL encryption to
                be used when opening connections to the IMAP server. Any
                other value will be considered as "do not use SSL"
            port: integer - Port number to connect to on the server. Keep in
                mind that most IMAP servers will have one port for standard
                connection and another one for encrypted connection (see
                use-ssl parameter above)
            type: string - Currently, the only supported type is IMAP

        Optional Arguments:
            origin_ip: string - IP address of the end user requesting the account
                to be created
            expunge_on_deleted_flag: integer - By default, we don't filter out messages
                flagged as deleted. Set this parameter to 1 to turn on this filtering.
            sync_all_folders: integer - By default, we filter out some folders like
                'Deleted Items' and 'Drafts'. Set this parameter to 1 to turn off this
                filtering and show every single folder.
            sync_folders: string - By default, we filter out some folders like
                'Deleted Items' and 'Drafts'. Set this parameter to
                'All,Trash' to show the 'Deleted Items' folder.
            sync_flags:  integer By default, we don't synchronize IMAP flags.
                Set this parameter to 1 to turn on IMAP flag syncing for the 'seen' and
                'flagged' flags.
            raw_file_list: integer - By default, we filter out files like
                signature images or those winmail.dat files form the files
                list. Set this parameter to 1 to turn off this filtering and
                show every single file attachments.
            password: string - Password for authentication on the IMAP server.
                Ignored if any of the provider_* parameters are set below.
            provider_refresh_token: An OAuth2 refresh token obtained from the
                IMAP account provider to be used to authenticate on this email
                account.
            provider_consumer_key: string - The OAuth consumer key used to
                obtain the the token and token secret above for that account.
                That consumer key and secret must be configured in your
                Context.IO account.
            callback_url: string (url) - If specified, we'll make a POST
                request to this URL when the initial sync is completed.
                status_callback_url: string (url) - If specified, we'll make a POST
                request to this URL if the connection status of the source changes.

        Returns:
            An Account object
        """
        req_args = ["email"]
        all_args = ["email", "migrate_account_id", "first_name", "last_name", "server",
            "username", "use_ssl", "port", "type", "origin_ip", "expunge_on_deleted_flag",
            "sync_all_folders", "sync_folders", "sync_flags", "raw_file_list", "password",
            "provider_refresh_token", "provider_consumer_key", "callback_url", "status_callback_url"
        ]

        params = helpers.sanitize_params(params, all_args, req_args)

        return Account(self, self._request_uri("accounts", method="POST", params=params))

    def get_connect_tokens(self, **params):
        """Get a list of connect tokens created with your API key.

        Documentation: http://context.io/docs/2.0/connect_tokens#get

        Optional Arguments:
            token : string - The connect token used to create the account .

        Making the api call https://context.io/2.0/connect_tokens/<token_id>

        Returns(if token is given):

        A dictionary :

        {
          "token": stringId of the connect_token,
          "email": stringemail address specified on token creation,
          "created": numberUnix timestamp of the connect_token was created,
          "used": numberUnix time this token was been used. 0 means it no account has been created with this token yet,
          "expires": mixedUnix time this token will expire and be purged. Once the token is used, this property will be set to false,
          "callback_url": stringURL of your app we'll redirect the browser to when the account is created,
          "first_name": stringFirst name specified on token creation,
          "last_name": stringLast name specified on token creation,
          "account": {
            If the connect_token hasn't been used yet, this object will be empty
            "id": stringId of the account created with this token,
            "created": numberUnix timestamp of account creation time,
            "suspended": numberUnix timestamp of account suspension time 0 means not suspended,
            "email_addresses":arrayArray of email addresses for this account. This only lists the actual addresses as strings.,
            "first_name": stringFirst name of account holder,
            "last_name": stringLast name of account holder,
            "sources": arrayList of sources this account gets data from. See sources
            If your key uses 3-legged signatures, the following 2 properties are added
            "access_token": stringOAuth access token to sign all future requests on this account,
            "access_token_secret": stringOAuth access token secret to sign all future requests on this account
          }
        }

        or

        Returns:
            A list of ConnectToken objects.
        """
        if params:
            return self._request_uri('connect_tokens'+'/'+params['token'])
        else:
            return [ConnectToken(self, obj) for obj in self._request_uri('connect_tokens')]

    def post_connect_token(self, **params):
        """Obtain a new connect token.

        Documentation: http://context.io/docs/2.0/connect_tokens#post

        Required Arguments:
            callback_url: string (url) - When the user's mailbox is connected
                to your API key, the browser will call this url (GET). This
                call will have a parameter called contextio_token indicating
                the connect_token related to this callback. You can then do a
                get on this connect_token to obtain details about the account
                and source created through that token and save that account id
                in your own user data.

        Optional Arguments:
            email: string - The email address of the account to be added. If
                specified, the first step of the connect UI where users are
                prompted for their email address, first name and last name is
                skipped.
            first_name: string - First name of the account holder.
            last_name: string - Last name of the account holder.
            source_callback_url: string - If specified, we'll make a POST
                request to this URL when the initial sync is completed.
            source_sync_all_folders: integer - By default, we filter out some
                folders like 'Deleted Items' and 'Drafts'. Set this parameter
                to 1 to turn off this filtering and show every single folder.
            source_sync_flags: integer - By default, we don't synchronize IMAP
                flags. Set this parameter to 1 to turn on IMAP flag syncing
                for the 'seen' and 'flagged' flags.
            source_raw_file_list: integer - By default, we filter out files
                like signature images from the files list. Set this parameter
                to 1 to turn off this filtering and show every single file
                attachment.
            status_callback_url: string (url) - If specified, we'll make a POST
            request to this URL if the connection status of the source changes.

        Returns:
            A dictionary, data format below

            {
              "success": string - true if connect_token was successfully
                  created, false otherwise,
              "token": string - Id of the token,
              "resource_url": string - URL to of the token,
              "browser_redirect_url": string - Redirect the user's browser to
                  this URL to have them connect their mailbox through this
                  token
            }
        """
        req_args = ['callback_url', ]
        all_args = [
            'callback_url', 'email', 'first_name', 'last_name',
            'source_callback_url', 'source_sync_all_folders',
            'source_sync_flags', 'source_raw_file_list', 'status_callback_url'
        ]

        params = helpers.sanitize_params(params, all_args, req_args)

        return self._request_uri('connect_tokens', method='POST', params=params)

    def get_discovery(self, **params):
        """Attempts to discover IMAP settings for a given email address.

        Documentation: http://context.io/docs/2.0/discovery

        Required Arguments:
            source_type: string - The type of source you want to discover
                settings for. Right now, the only supported source type is IMAP
            email: string - An email address you want to discover IMAP
                settings for. Make sure source_type is set to IMAP.

        Returns:
            A Discovery object.
        """
        if 'source_type' not in params:
            params['source_type'] = 'IMAP'

        req_args = ['source_type', 'email']
        all_args = ['source_type', 'email']

        params = helpers.sanitize_params(params, all_args, req_args)

        return Discovery(self, self._request_uri('discovery', params=params))

    def get_oauth_providers(self):
        """List of oauth providers configured.

        Documentation: http://context.io/docs/2.0/oauth_providers#get

        Arguments:
            None

        Returns:
            A list of OauthProvider objects.
        """
        return [OauthProvider(self, obj) for obj in self._request_uri('oauth_providers')]

    def post_oauth_provider(self, **params):
        """Add a new OAuth provider.

        Required Arguments:
            type: string -  Identification of the OAuth provider. This must be
                either GMAIL and GOOGLEAPPSMARKETPLACE.
            provider_consumer_key: string - The OAuth consumer key
            provider_consumer_secret: string - The OAuth consumer secret

        Returns:
            a dictionary
        """
        req_args = [
            'type', 'provider_consumer_key', 'provider_consumer_secret']
        all_args = [
            'type', 'provider_consumer_key', 'provider_consumer_secret']

        params = helpers.sanitize_params(params, all_args, req_args)

        return self._request_uri('oauth_providers', method='POST', params=params)
