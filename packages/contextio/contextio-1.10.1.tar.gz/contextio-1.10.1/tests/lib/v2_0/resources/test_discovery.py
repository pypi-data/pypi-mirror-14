import unittest

from contextio.contextio import ContextIO
from contextio.lib.v2_0.resources.discovery import Discovery


class TestDiscoveryResource(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")
        self.discovery = Discovery(self.contextio, {})

    def test_constructor_creates_discovery_object_with_all_attributes_in_keys_list(self):
        self.assertTrue(hasattr(self.discovery, 'email'))
        self.assertTrue(hasattr(self.discovery, 'found'))
        self.assertTrue(hasattr(self.discovery, 'type'))
        self.assertTrue(hasattr(self.discovery, 'imap'))
        self.assertTrue(hasattr(self.discovery, 'documentation'))
