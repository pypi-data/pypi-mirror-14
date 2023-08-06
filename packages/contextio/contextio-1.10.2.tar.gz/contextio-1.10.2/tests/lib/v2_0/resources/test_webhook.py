import unittest

from contextio.contextio import ContextIO
from contextio.lib.v2_0.resources.account import Account
from contextio.lib.v2_0.resources.webhook import WebHook


class TestWebHookResource(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")
        self.account = Account(self.contextio, {"id": "fake_id"})

        self.webhook = WebHook(self.account, {"webhook_id": "fake_webhook_id"})

    def test_constructor_creates_message_object_with_all_attributes_in_keys_list(self):
        self.assertTrue(hasattr(self.webhook, "callback_url"))
        self.assertTrue(hasattr(self.webhook, "failure_notif_url"))
        self.assertTrue(hasattr(self.webhook, "active"))
        self.assertTrue(hasattr(self.webhook, "failure"))
        self.assertTrue(hasattr(self.webhook, "webhook_id"))
        self.assertTrue(hasattr(self.webhook, "filter_to"))
        self.assertTrue(hasattr(self.webhook, "filter_from"))
        self.assertTrue(hasattr(self.webhook, "filter_cc"))
        self.assertTrue(hasattr(self.webhook, "filter_subject"))
        self.assertTrue(hasattr(self.webhook, "filter_thread"))
        self.assertTrue(hasattr(self.webhook, "filter_new_important"))
        self.assertTrue(hasattr(self.webhook, "filter_file_name"))
        self.assertTrue(hasattr(self.webhook, "filter_folder_added"))
        self.assertTrue(hasattr(self.webhook, "filter_folder_removed"))
        self.assertTrue(hasattr(self.webhook, "filter_to_domain"))
        self.assertTrue(hasattr(self.webhook, "filter_from_domain"))
