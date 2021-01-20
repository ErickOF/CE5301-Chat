import socket
import select


MAX_BUFFER_SIZE: int = 4096
PORT: int = 5001
HOST: str = "127.0.0.1"
MAX_CONNECTIONS: int = 10

# List to keep track of socket descriptors
connectedClients: list = []

name: str = ""
# Dictionary to store address corresponding to username
addresses: dict = {}


def sendToAll(serverSocket, sock, message: str) -> None:
    """Send message to all connected clients in the server.
    """
    for socket in connectedClients:
        # Not send to itself
        if socket != serverSocket and socket != sock:
            try:
                socket.send(message.encode())
            except:
                # If connection not available, close and remove socket
                socket.close()
                connectedClients.remove(socket)


def runServer():
    """Start running server.
    """
    serverSocket: socket.socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

    serverSocket.bind((HOST, PORT))
    serverSocket.listen(MAX_CONNECTIONS)

    # Add server socket to the list of readable connections
    connectedClients.append(serverSocket)

    print("\33[32mSERVER WORKING..\33[0m")

    running: bool = True

    while running:
        # Get the list sockets which are ready to be read through select
        rList, wList, _ = select.select(connectedClients, [], [])

        for sock in rList:
            # New connection
            if sock == serverSocket:
                # Handle the case in which there is a new connection received
                # through server socket
                sockfd, addr = serverSocket.accept()

                # User name
                name = sockfd.recv(MAX_BUFFER_SIZE).decode()

                # Repeated username
                if name in addresses.values():
                    sockfd.send(
                        "\r\33[31m\33[1m Username already exist!\n\33[0m".encode())

                    sockfd.close()
                else:
                    # Add new client
                    connectedClients.append(sockfd)
                    # Add name and address
                    addresses[addr] = name

                    print(f"Client ({addr}, {addresses[addr]}) connected")

                    sockfd.send(
                        "\33[32m\r\33[1m Welcome to chat room. Enter '$exit' to exit...\n\33[0m".encode())

                    sendToAll(
                        serverSocket, sockfd, f"\33[32m\33[1m\r {name} joined the conversation :) \n\33[0m")
            else:
                # Some incoming message from a client
                try:
                    # Data from client
                    data: str = sock.recv(MAX_BUFFER_SIZE).decode()
                    data = data[:data.index("\n")]

                    # Get address of client sending the message
                    i, p = sock.getpeername()

                    # Exit signal
                    if data == "$exit":
                        msg: str = f"\r\33[1m\33[31m {addresses[(i, p)]} left the conversation :( \33[0m\n"

                        sendToAll(serverSocket, sock, msg)

                        print(
                            f"Client ({i}, {p}) is offline [{addresses[(i, p)]}")

                        del addresses[(i, p)]

                        connectedClients.remove(sock)
                        sock.close()
                    else:
                        msg = f"\r\33[1m\33[35m {addresses[(i, p)]} : \33[0m{data}\n"

                        sendToAll(serverSocket, sock, msg)

                # Abrupt user exit
                except:
                    (i, p) = sock.getpeername()

                    sendToAll(
                        serverSocket, sock, "\r\33[31m \33[1m "
                        + f"{addresses[(i, p)]} left the  "
                        + "unexpectedly :() \33[0m\n")

                    print(
                        f"Client ({i}, {p}) is offline (error) [{addresses[(i, p)]}]\n")

                    del addresses[(i, p)]

                    connectedClients.remove(sock)
                    sock.close()

    serverSocket.close()


if __name__ == "__main__":
    runServer()
