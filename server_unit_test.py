import unittest
import socket
from time import sleep
import mock
import server


def accept_gen():
    for i in range(1):
        mock_socket = mock.MagicMock(name='socket.socket', spec=socket.socket)
        sleep(1)
        yield (mock_socket, ['0.0.0.0', 5001])
    while True:
        sleep(1)
        yield socket.error()

@mock.patch('socket.socket', autospec=True)
def test_listen_tcp(mock_socket):
    mocked_socket = mock_socket.return_value
    mocked_socket.accept.side_effect = accept_gen()

    server.runServer()

    mock_socket.assert_called_once()
    
    print("Test passed")

if __name__ == "__main__":
    test_listen_tcp()
