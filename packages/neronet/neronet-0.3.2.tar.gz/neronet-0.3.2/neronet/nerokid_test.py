import unittest
import socket
import neronet.nerokid
import os
import sys

class TestSpecifyExperiments(unittest.TestCase):

    def test_server_gets_data(self):
        sock = socket.socket()
        sock.settimeout(5.0)
        sock.bind(('localhost', 0))
        sock.listen(1)
        host, port = sock.getsockname()
        sys.argv = ["nerokid.py", host, str(port), "sleep.py", "1", "1"]
        testKid = neronet.nerokid.NeroKid()
        testKid.run()
        newsock, asd = sock.accept()
        data = newsock.recv(2048)
        sock.close()
        newsock.close()
        self.assertTrue(data)

    def test_socket_initialize_success(self):
        sys.argv = ["nerokid.py", "localhost", "0"]
        testKid = neronet.nerokid.NeroKid()
        testKid.initialize_socket()

if __name__ == '__main__':
    unittest.main()