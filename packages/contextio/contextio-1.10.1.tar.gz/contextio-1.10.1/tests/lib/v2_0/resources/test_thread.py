import unittest

from contextio.contextio import ContextIO
from contextio.lib.v2_0.resources.account import Account
from contextio.lib.v2_0.resources.message import Message
from contextio.lib.v2_0.resources.thread import Thread
from contextio.lib.v2_0.resources.source import Source


class TestSourceResource(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")
        self.account = Account(self.contextio, {"id": "fake_id"})
        self.thread = Thread(self.account, {"gmail_thread_id": "foobar"})

    def test_constructor_creates_thread_object_with_all_attributes_in_keys_list(self):
        self.assertTrue(hasattr(self.thread, "gmail_thread_id"))
        self.assertTrue(hasattr(self.thread, "email_message_ids"))
        self.assertTrue(hasattr(self.thread, "person_info"))
        self.assertTrue(hasattr(self.thread, "messages"))
        self.assertTrue(hasattr(self.thread, "subject"))
        self.assertTrue(hasattr(self.thread, "folders"))
        self.assertTrue(hasattr(self.thread, "sources"))

    def test_constructor_adds_messages_to_thread_object_if_messages_in_definition(self):
        thread = Thread(self.account, {
            "gmail_thread_id": "foobar",
            "messages": [
                {"message_id": "foo"},
                {"message_id": "bar"}
            ]
        })

        self.assertIsInstance(thread.messages[0], Message)
        self.assertIsInstance(thread.messages[1], Message)

    def test_constructor_adds_sources_to_thread_object_if_sources_in_definition(self):
        thread = Thread(self.account, {
            "gmail_thread_id": "foobar",
            "sources": [
                {"label": "foo"},
                {"label": "bar"}
            ]
        })

        self.assertIsInstance(thread.sources[0], Source)
        self.assertIsInstance(thread.sources[1], Source)
