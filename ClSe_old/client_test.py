import unittest
import client


class Testclient(unittest.TestCase):
    def setUp(self):
        self.s = client.get_server_socket('localhost', 7777)
        self.c = client.get_client_socket('localhost', 7777)
        self.sender = self.s.accept()[0]

        client.send_data(self.c, {'test': 'test'})

    def tearDown(self):
        self.c.close()
        self.s.close()

    def test_get_data(self):
        self.assertEqual(client.get_data(self.sender), {'test': 'test'})

    def test_send_data(self):
        with self.assertRaises(TypeError):
            client.send_data()


if __name__ == '__main__':
    unittest.main()