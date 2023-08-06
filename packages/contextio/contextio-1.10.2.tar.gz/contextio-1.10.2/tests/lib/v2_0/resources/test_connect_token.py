from mock import Mock
import unittest

from contextio.contextio import ContextIO
from contextio.lib.v2_0.resources.account import Account
from contextio.lib.v2_0.resources.connect_token import ConnectToken

class TestConnectTokenResource(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")
        self.account = Account(self.contextio, {"id": "fake_id"})

        self.connect_token = ConnectToken(self.account, {"token": "fake_token"})
        self.uri = "https://api.context.io/2.0/accounts/fake_id/sources/foobar/folders/fake_folder_name/"

    def test_constructor_creates_connect_token_object_with_all_attributes_in_keys_list(self):
        self.assertTrue(hasattr(self.connect_token, "token"))
        self.assertTrue(hasattr(self.connect_token, "email"))
        self.assertTrue(hasattr(self.connect_token, "created"))
        self.assertTrue(hasattr(self.connect_token, "used"))
        self.assertTrue(hasattr(self.connect_token, "expires"))
        self.assertTrue(hasattr(self.connect_token, "callback_url"))
        self.assertTrue(hasattr(self.connect_token, "first_name"))
        self.assertTrue(hasattr(self.connect_token, "last_name"))
        self.assertTrue(hasattr(self.connect_token, "account"))

    def test_constructor_sets_account_attribute_to_none_if_empty_dict(self):
        definition = {
            "token": "fake_token",
            "email": "fake@email.com",
            "created": 1458569718,
            "used": 1458569718,
            "expires": False,
            "callback_url": "https://some.url",
            "first_name": "fake",
            "last_name": "name",
            "account": {}
        }

        account = Account(Mock(), {"id": "fake_id"})
        connect_token = ConnectToken(account, definition)

        self.assertEqual(None, connect_token.account)
