import socket
import threading


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return "Error: " + str(e)


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Accepted connection from {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            self.clients.append((client_socket, client_thread))
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break

                print(f"Received message: {message}")

                if message.lower() == "disconnect":
                    self.disconnect_client(client_socket)
                    break

                # You can implement your own logic he re to process the message.
                # For example, you can send a response back to the client.

            except Exception as e:
                print(f"Error handling client: {e}")
                self.disconnect_client(client_socket)
                break

    def disconnect_client(self, client_socket):
        print(f"Disconnecting client {client_socket.getpeername()}")
        client_socket.close()
        self.clients = [(c_socket, c_thread) for c_socket, c_thread in self.clients if c_socket != client_socket]


if __name__ == "__main__":
    server = Server(get_ip_address(), 8003)
    server.start()
