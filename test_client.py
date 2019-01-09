from unittest import TestCase
from Client.Client import Client


class TestClient(TestCase):

    def test_close_client(self):
        obj = Client("user")
        self.assertEqual(obj.close_client(), 0)
        obj.close_client()

    def test_send_message(self):
        obj = Client("user")

        # Test wrong types
        self.assertRaises(TypeError, obj.send_message, list())
        self.assertRaises(TypeError, obj.send_message, int())

        # Test bytes
        self.assertEqual(obj.send_message("test message"), 0)

        obj.close_client()

    def test_receiving(self):
        pass
