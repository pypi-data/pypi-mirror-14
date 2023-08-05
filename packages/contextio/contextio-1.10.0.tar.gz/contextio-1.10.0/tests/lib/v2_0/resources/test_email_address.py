from mock import patch
import unittest

from contextio.contextio import ContextIO
from contextio.lib.v2_0.resources.email_address import EmailAddress


class TestEmailAddressResource(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")
        self.email_address = EmailAddress(self.contextio, {
            "email": "fake@email.com",
            "validated": 1234567890,
            "primary": 1
        })

    def test_constructor_sets_attributes_on_object(self):
        self.assertTrue(hasattr(self.email_address, "email"))
        self.assertTrue(hasattr(self.email_address, "validated"))
        self.assertTrue(hasattr(self.email_address, "primary"))


    def test_constructor_allows_email_address_in_definition(self):
        email_address = EmailAddress(self.contextio, {"email_address": "fake@email.com"})

        self.assertEqual("fake@email.com", email_address.email)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource.post")
    def test_post_updates_primary_attribute_in_memory(self, mock_post):
        self.assertEqual(self.email_address.primary, 1)

        self.email_address.post(primary=0)

        self.assertEqual(self.email_address.primary, 0)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource.post")
    def test_post_attempts_to_convert_string_input_to_int(self, mock_post):
        self.assertEqual(self.email_address.primary, 1)

        self.email_address.post(primary="0")

        self.assertEqual(self.email_address.primary, 0)

    def test_post_throws_error_if_unable_to_parse_int(self):
        self.assertEqual(self.email_address.primary, 1)

        with self.assertRaises(ValueError):
            self.email_address.post(primary="not_integer")
