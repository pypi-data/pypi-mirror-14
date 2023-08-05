import json
import mock
import unittest
from contextio.contextio import ContextIO
from requests.exceptions import HTTPError
from rauth import OAuth1Session


import contextio.lib.v2_0.errors as errors
from contextio.lib.v2_0.resources.account import Account
from contextio.lib.v2_0.resources.connect_token import ConnectToken
from contextio.lib.v2_0.resources.discovery import Discovery
from contextio.lib.v2_0.resources.oauth_provider import OauthProvider

class TestContextIO(unittest.TestCase):
    def setUp(self):
        # some of the following tests mock the OAuth session created in the constructor
        # in for these tests we must redeclare self.contextio
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")

    def test_constructor_creates_object_with_default_config(self):
        self.assertEqual("foo", self.contextio.consumer_key)
        self.assertEqual("bar", self.contextio.consumer_secret)
        self.assertEqual("https://api.context.io", self.contextio.url_base)
        self.assertEqual("2.0", self.contextio.version)
        self.assertEqual(None, self.contextio.debug)
        self.assertIsInstance(self.contextio.session, OAuth1Session)

    def test_constructor_creates_object_with_custom_config(self):
        self.contextio = ContextIO(
            consumer_key="foo",
            consumer_secret="bar",
            url_base="http://fake.url",
            debug="print",
            version="lite"
        )

        self.assertEqual("foo", self.contextio.consumer_key)
        self.assertEqual("bar", self.contextio.consumer_secret)
        self.assertEqual("http://fake.url", self.contextio.url_base)
        self.assertEqual("lite", self.contextio.version)
        self.assertEqual("print", self.contextio.debug)

    def test_constructor_maps_True_to_print_for_debug_value(self):
        self.contextio = ContextIO(
            consumer_key="foo",
            consumer_secret="bar",
            debug=True
        )

        self.assertEqual("foo", self.contextio.consumer_key)
        self.assertEqual("bar", self.contextio.consumer_secret)
        self.assertEqual("print", self.contextio.debug)

    @mock.patch("contextio.contextio.six.print_")
    def test_debug_prints_message_when_debug_equals_print(self, mock_six_print):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar", debug="print")
        mock_response = mock.Mock()
        mock_response.request.url = "fake_url"
        mock_response.request.method = "GET"
        mock_response.status_code = 404

        message = (
            "--------------------------------------------------\n"
            "URL:    {0}\nMETHOD: {1}\nSTATUS: 2\n\nREQUEST\n{3}\n\nRESPON"
            "SE\n{4}\n").format(
                mock_response.request.url, mock_response.request.method, mock_response.status_code,
                mock_response.request.__dict__, mock_response.__dict__)

        self.contextio._debug(mock_response)

        mock_six_print.assert_called_with(message)

    @mock.patch("contextio.contextio.logging.debug")
    def test_debug_logs_message_when_debug_equals_log(self, mock_logging_debug):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar", debug="log")
        mock_response = mock.Mock()
        mock_response.request.url = "fake_url"
        mock_response.request.method = "GET"
        mock_response.status_code = 404
        message = (
            "--------------------------------------------------\n"
            "URL:    {0}\nMETHOD: {1}\nSTATUS: 2\n\nREQUEST\n{3}\n\nRESPON"
            "SE\n{4}\n").format(
                mock_response.request.url, mock_response.request.method, mock_response.status_code,
                mock_response.request.__dict__, mock_response.__dict__)

        self.contextio._debug(mock_response)

        mock_logging_debug.assert_called_with(message)

    @mock.patch("contextio.contextio.pkg_resources")
    @mock.patch("contextio.contextio.OAuth1Session")
    def test_request_defaults_to_GET_method_and_include_user_agent_header(self, mock_session, mock_pkg_resources):
        mock_package = mock.Mock()
        mock_package.version = "v1.0.0"
        mock_pkg_resources.require.return_value = [mock_package]

        mock_session.return_value.request = mock.Mock()
        mock_request = mock_session.return_value.request

        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")

        with self.assertRaises(HTTPError):
            self.contextio._request_uri("catpants")

        mock_request.assert_called_with(
            "GET", "https://api.context.io/2.0/catpants",
            data="",
            header_auth=True,
            headers={'user-agent': 'contextio/2.0/python-lib-v1.0.0'},
            params={}
        )

    @mock.patch("contextio.contextio.ContextIO._request_uri")
    def test_request_uri_raises_HTTPError_if_status_not_between_200_and_300(self, mock_request):
        mock_request.side_effect = HTTPError

        with self.assertRaises(HTTPError):
            self.contextio._request_uri("catpants")

    @mock.patch("contextio.contextio.OAuth1Session")
    def test_request_uri_returns_response_content_if_UnicodeDecodeError_raised(self, mock_session):
        mock_request = mock_session.return_value.request.return_value
        mock_request.json.side_effect = UnicodeDecodeError("", "", 42, 43, "")
        mock_request.status_code = 200
        mock_request.content = bytes("foo bar")

        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")

        response = self.contextio._request_uri("catpants")

        self.assertEqual("foo bar", response)

    @mock.patch("contextio.contextio.OAuth1Session")
    def test_request_uri_returns_response_text_if_ValueError_raised(self, mock_session):
        mock_request = mock_session.return_value.request.return_value
        mock_request.status_code = 200
        mock_request.json.side_effect = ValueError()
        mock_request.text = "This is some text"

        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")

        response = self.contextio._request_uri("catpants")
        self.assertEqual("This is some text", response)

    @mock.patch("contextio.contextio.ContextIO._request_uri")
    def test_request_uri_returns_json(self, mock_request):
        mock_request.return_value = ({"foo": "bar"})

        response = self.contextio._request_uri("catpants")

        self.assertEqual({"foo": "bar"}, response)

    @mock.patch("contextio.contextio.pkg_resources")
    @mock.patch("contextio.contextio.OAuth1Session")
    def test_request_includes_body_if_method_is_POST(self, mock_session, mock_pkg_resources):
        mock_package = mock.Mock()
        mock_package.version = "v1.0.0"
        mock_pkg_resources.require.return_value = [mock_package]

        mock_request = mock_session.return_value.request
        mock_request.return_value.status_code = 200

        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar", version="some_version")

        self.contextio._request_uri("catpants", method="POST", body=json.dumps({"foo": "bar"}))

        mock_request.assert_called_with(
            "POST", "https://api.context.io/some_version/catpants",
            data={"body": '{"foo": "bar"}'},
            header_auth=True,
            headers={'user-agent': 'contextio/some_version/python-lib-v1.0.0'}
        )

    @mock.patch("contextio.contextio.ContextIO._request_uri")
    def test_get_accounts_returns_list_of_Account_resources(self, mock_request):
        mock_request.return_value = {"id": "some_id"}
        accounts = self.contextio.get_accounts()

        self.assertEqual(1, len(accounts))
        self.assertIsInstance(accounts[0], Account)

    @mock.patch("contextio.contextio.ContextIO._request_uri")
    def test_post_account_returns_Account_object(self, mock_request):
        mock_request.return_value = {"id": "some_id"}

        account = self.contextio.post_account(email="fake@email.com")

        self.assertIsInstance(account, Account)

    @mock.patch("contextio.contextio.ContextIO._request_uri")
    def test_get_connect_tokens_returns_list_of_ConnectToken_resources_without_token(self, mock_request):
        mock_request.return_value = [{"token": "fake_token", "account": {"id": "account_id"}}]

        connect_tokens = self.contextio.get_connect_tokens()

        self.assertEqual(1, len(connect_tokens))
        self.assertIsInstance(connect_tokens[0], ConnectToken)

    @mock.patch("contextio.contextio.ContextIO._request_uri")
    def test_get_connect_tokens_returns_dictionary_if_token_is_provided(self, mock_request):
        mock_request.return_value = {"token": "fake_token"}

        connect_token = self.contextio.get_connect_tokens(token="fake_token")

        self.assertEqual({"token": "fake_token"}, connect_token)


    @mock.patch("contextio.contextio.ContextIO._request_uri")
    def test_post_connect_token_requires_callback_url(self, mock_request):
        mock_request.return_value = {"token": "fake_token"}

        with self.assertRaises(errors.ArgumentError):
            self.contextio.post_connect_token()

    @mock.patch("contextio.contextio.ContextIO._request_uri")
    def test_post_connect_token_returns_dictionary(self, mock_request):
        mock_request.return_value = {"token": "fake_token"}

        connect_token = self.contextio.post_connect_token(callback_url="http://some.callback.url")

        self.assertEqual({"token": "fake_token"}, connect_token)

    @mock.patch("contextio.contextio.ContextIO._request_uri")
    def test_get_discovery_returns_discovery_object(self, mock_request):
        mock_request.return_value = {"email": "fake@email.com"}


        discovery = self.contextio.get_discovery(email="fake@email.com")

        self.assertIsInstance(discovery, Discovery)

    @mock.patch("contextio.contextio.ContextIO._request_uri")
    def test_get_discovery_requires_email_argument(self, mock_request):
        with self.assertRaises(errors.ArgumentError):
            self.contextio.get_discovery()

    @mock.patch("contextio.contextio.ContextIO._request_uri")
    def test_get_oauth_providers_returns_list_of_OauthProvider_objects(self, mock_request):
        mock_request.return_value = [{"provider_consumer_key": "1234"}]

        oauth_providers = self.contextio.get_oauth_providers()

        self.assertEqual(1, len(oauth_providers))
        self.assertIsInstance(oauth_providers[0], OauthProvider)

    @mock.patch("contextio.contextio.ContextIO._request_uri")
    def test_post_oauth_provider_returns_dictionary(self, mock_request):
        mock_request.return_value = {"provider_consumer_key": "123"}

        oauth_provider = self.contextio.post_oauth_provider(type="VALIDOAUTHTYPE", provider_consumer_key="1234", provider_consumer_secret="1234")

        self.assertEqual({"provider_consumer_key": "123"}, oauth_provider)

    @mock.patch("contextio.contextio.ContextIO._request_uri")
    def test_post_oauth_provider_requires_type_provider_key_and_provider_secret(self, mock_request):
        mock_request.return_value = {"provider_consumer_key": "123"}

        with self.assertRaises(errors.ArgumentError):
            self.contextio.post_oauth_provider()


