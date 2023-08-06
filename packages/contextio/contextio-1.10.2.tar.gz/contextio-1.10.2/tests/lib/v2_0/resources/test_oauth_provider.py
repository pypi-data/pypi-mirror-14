import unittest

from contextio.contextio import ContextIO
from contextio.lib.v2_0.resources.oauth_provider import OauthProvider


class TestOauthProviderResource(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")
        self.oauth_provider = OauthProvider(self.contextio, {"provider_consumer_key": "foobar"})

    def test_constructor_creates_message_object_with_all_attributes_in_keys_list(self):
        self.assertTrue(hasattr(self.oauth_provider, "type"))
        self.assertTrue(hasattr(self.oauth_provider, "provider_consumer_key"))
        self.assertTrue(hasattr(self.oauth_provider, "provider_consumer_secret"))
        self.assertTrue(hasattr(self.oauth_provider, "resource_url"))
