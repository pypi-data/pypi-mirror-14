import unittest
from mock import patch

from contextio.contextio import ContextIO
from contextio.lib.v2_0.resources.account import Account
from contextio.lib.v2_0.resources.message import Message
from contextio.lib.v2_0.resources.thread import Thread


class TestMessageResource(unittest.TestCase):
    def setUp(self):
        self.contextio = ContextIO(consumer_key="foo", consumer_secret="bar")
        self.account = Account(self.contextio, {"id": "fake_id"})

        self.message = Message(self.account, {"message_id": "fake_message_id"})

    def test_constructor_creates_message_object_with_all_attributes_in_keys_list(self):
        self.assertTrue(hasattr(self.message, 'date'))
        self.assertTrue(hasattr(self.message, 'date_indexed'))
        self.assertTrue(hasattr(self.message, 'addresses'))
        self.assertTrue(hasattr(self.message, 'person_info'))
        self.assertTrue(hasattr(self.message, 'email_message_id'))
        self.assertTrue(hasattr(self.message, 'message_id'))
        self.assertTrue(hasattr(self.message, 'gmail_message_id'))
        self.assertTrue(hasattr(self.message, 'gmail_thread_id'))
        self.assertTrue(hasattr(self.message, 'files'))
        self.assertTrue(hasattr(self.message, 'subject'))
        self.assertTrue(hasattr(self.message, 'folders'))
        self.assertTrue(hasattr(self.message, 'sources'))


    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource.post")
    def test_post_sends_params_and_returns_True(self, mock_post):
        params = {
            "flag_answered": 0,
            "flag_draft": 0,
            "dst_folder": "foo",
            "dst_source": "bar",
            "move": 0,
            "flag_seen": 0,
            "flag_flagged": 0,
            "flag_deleted": 0
        }
        all_args = ['flag_answered', 'move', 'dst_folder', 'dst_source', 'flag_seen',
            'flag_flagged', 'flag_deleted', 'flag_draft']

        self.message.post(**params)

        mock_post.assert_called_with(
            all_args=all_args, params=params, required_args=['dst_folder'], return_bool=True)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource.post")
    def test_post_is_called_with_correct_args(self, mock_post):
        mock_post.return_value = {"success": True}
        req_args = ['dst_folder', ]
        all_args = [
            'flag_answered', 'move', 'dst_folder', 'dst_source', 'flag_seen',
            'flag_flagged', 'flag_deleted', 'flag_draft'
        ]

        self.message.post(return_bool=False, dst_folder="foobar")

        mock_post.assert_called_with(return_bool=False, params={"dst_folder": "foobar"}, all_args=all_args, required_args=req_args)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource._request_uri")
    def test_delete_returns_boolean(self, mock_request):
        deleted_message = self.message.delete()

        self.assertEqual(True, deleted_message)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource._request_uri")
    def test_get_body_returns_list_of_dictionaries(self, mock_request):
        mock_request.return_value = [{"foo": "bar"}]

        response = self.message.get_body(type="foobar")

        mock_request.assert_called_with("body", params={"type": "foobar"})
        self.assertEqual(1, len(response))
        self.assertEqual([{"foo": "bar"}], response)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource._request_uri")
    def test_get_flags_returns_a_dictionary(self, mock_request):
        mock_request.return_value = {"foo": "bar"}

        response = self.message.get_flags()

        mock_request.assert_called_with("flags")
        self.assertEqual({"foo": "bar"}, self.message.flags)
        self.assertEqual({"foo": "bar"}, response)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource._request_uri")
    def test_post_flag_calls_request_uri_with_correct_args(self, mock_request):
        params = {"seen":1, "answered":1, "flagged":1, "deleted":0, "draft":1}
        mock_request.return_value = {"success": True, "flags": ["foo", "bar"]}

        response = self.message.post_flag(**params)

        mock_request.assert_called_with("flags", method="POST", params=params)
        self.assertEqual(["foo", "bar"], self.message.flags)
        self.assertTrue(response)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource._request_uri")
    def test_get_folders_returns_a_list_of_dictionaries(self, mock_request):
        mock_request.return_value = [{"foo": "bar"}]

        response = self.message.get_folders()

        mock_request.assert_called_with("folders")
        self.assertEqual([{"foo": "bar"}], self.message.folders)
        self.assertEqual([{"foo": "bar"}], response)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource.post")
    def test_post_folder_calls_request_uri_with_correct_args(self, mock_request):
        params = {"add": "catpants", "remove": "dogpants"}
        mock_request.return_value = {"success": True}

        response = self.message.post_folder(**params)

        mock_request.assert_called_with("folders", params=params)

        self.assertTrue(response)


    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource._request_uri")
    def test_put_folders_calls_request_uri_with_correct_args(self, mock_request):
        body = "catpants"
        mock_request.return_value = {"success": True, "flags": ["foo", "bar"]}

        response = self.message.put_folders(body)

        mock_request.assert_called_with("folders", method="PUT", body=body)
        self.assertEqual("catpants", self.message.folders)
        self.assertTrue(response)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource._request_uri")
    def test_get_headers_returns_a_dictionary(self, mock_request):
        mock_request.return_value = {"foo": "bar"}

        response = self.message.get_headers(raw=1)

        mock_request.assert_called_with("headers", params={"raw": 1})
        self.assertEqual({"foo": "bar"}, self.message.headers)
        self.assertEqual({"foo": "bar"}, response)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource._request_uri")
    def test_get_source_returns_a_string(self, mock_request):
        mock_request.return_value = "catpants"

        response = self.message.get_source()

        mock_request.assert_called_with("source")
        self.assertEqual("catpants", self.message.source)
        self.assertEqual("catpants", response)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource._request_uri")
    def test_get_thread_returns_response_body_object_when_thread_id_exists(self, mock_request):
        mock_request.return_value = "catpants"

        response = self.message.get_source()

        mock_request.assert_called_with("source")
        self.assertEqual("catpants", self.message.source)
        self.assertEqual("catpants", response)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource._request_uri")
    def test_get_thread_returns_a_Thread_object_when_thread_id_exists(self, mock_request):
        mock_request.return_value = {
            "messages": [{"message_id": "foo","gmail_thread_id": "foobar"}]
        }

        params = {
            "include_body": 1,
            "include_headers": 1,
            "include_flags": 1,
            "body_type": "foobar",
            "limit": 1,
            "offset": 1
        }

        response = self.message.get_thread(**params)

        mock_request.assert_called_with("thread", params=params)
        self.assertEqual(response, self.message.thread)
        self.assertIsInstance(response, Thread)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource._request_uri")
    def test_get_thread_returns_response_body_when_thread_id_does_not_exist(self, mock_request):
        mock_request.return_value = {"foo": "bar"}
        params = {
            "include_body": 1,
            "include_headers": 1,
            "include_flags": 1,
            "body_type": "foobar",
            "limit": 1,
            "offset": 1
        }
        response = self.message.get_thread(**params)

        mock_request.assert_called_with("thread", params=params)
        self.assertEqual({"foo": "bar"}, self.message.thread)
        self.assertEqual({"foo": "bar"}, response)

    @patch("contextio.lib.v2_0.resources.base_resource.BaseResource._request_uri")
    def test_get_thread_sets_thread_subject_if_message_has_subject(self, mock_request):
        mock_request.return_value = {

                "messages": [{"message_id": "foo", "gmail_thread_id": "foobar"}
            ]

        }
        params = {
            "include_body": 1,
            "include_headers": 1,
            "include_flags": 1,
            "body_type": "foobar",
            "limit": 1,
            "offset": 1

        }
        message = Message(self.account, {"message_id": "fake_message_id", "subject": "catpants"})
        message.get_thread(**params)

        self.assertEqual("catpants", message.thread.subject)



