import socket
import select
import string
import sys


MAX_BUFFER_SIZE: int = 4096
PORT: int = 5001
TIMEOUT: int = 2


def display():
    """Display the message
    """
    you = "\33[33m\33[1m You: \33[0m"
    sys.stdout.write(you)
    sys.stdout.flush()


def run():
    host: str = input("Enter host IP address: ")

    # Asks for user name
    name: str = input("\33[34m\33[1m Enter username: \33[0m")

    # Create socket
    s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)

    try:
        # Connecting host
        s.connect((host, PORT))
    except:
        print("\33[31m\33[1m Can't connect to the server. \33[0m")

        s.close()
        sys.exit()

    # Send data
    s.send(name.encode())
    # Print you
    display()

    running: bool = True

    while running:
        socketList = [sys.stdin, s]

        # Get the list of sockets which are readable
        rList, wList, _ = select.select(socketList, [], [])

        for sock in rList:
            # Incoming message from server
            if sock == s:
                # Get data from server
                data: str = sock.recv(MAX_BUFFER_SIZE).decode()

                if not data:
                    print('\33[31m\33[1m \rDISCONNECTED!!!\n \33[0m')
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    display()
            else:
                # Read and send user messsage
                msg = sys.stdin.readline().encode()
                s.send(msg)
                display()


if __name__ == "__main__":
    run()
