import unittest
import neronet.neromum
import socket
import os
import pickle


class Neromum_test(unittest.TestCase):

    def setUp(self):
        self.mum = neronet.neromum.Neromum()
        self.mum.experiment = 'sleep.py'
        self.d = {
            "log_output": {
                1: "stdout",
                2: "test\n\n\ni\n"},
            "running": False}
        self.data = pickle.dumps(self.d)
        self.mum.initialize_socket()

    def test_socket_init(self):

        self.assertTrue(self.mum.sock)
        self.assertTrue(isinstance(self.mum.port, int))
        self.assertEqual(self.mum.host, '127.0.0.1')
        self.assertEqual(self.mum.open_incoming_connections, [self.mum.sock])
        self.assertEqual(self.mum.open_outgoing_connections, [])

    def test_parse_data(self):

        self.mum.data = self.data
        self.mum.parse_nerokid_data()
        self.assertEqual(self.mum.data, self.d)

if __name__ == '__main__':
    unittest.main()
