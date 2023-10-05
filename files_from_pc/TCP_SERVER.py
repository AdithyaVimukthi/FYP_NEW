import socket
import threading
import cv2
import imutils
import pickle
import struct


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
        self.vid = None
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            self.client_socket, client_address = self.server_socket.accept()
            print(f"Accepted connection from {client_address}")
            client_thread = threading.Thread(target=self.handle_client)
            self.clients.append((self.client_socket, client_thread))
            client_thread.start()

    def handle_client(self):
        self.vid = cv2.VideoCapture(0)
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break
                self.send_video()

                print(f"Received message: {message}")

                if message.lower() == "disconnect":
                    self.disconnect_client()
                    break

                # You can implement your own logic he re to process the message.
                # For example, you can send a response back to the client.

            except Exception as e:
                print(f"Error handling client: {e}")
                self.disconnect_client()
                break

    def send_video(self):
        img, frame = self.vid.read()
        frame = imutils.resize(frame, width=320)
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        self.client_socket.sendall(message)

    def disconnect_client(self):
        print(f"Disconnecting client {self.client_socket.getpeername()}")
        self.client_socket.close()
        self.clients = [(c_socket, c_thread) for c_socket, c_thread in self.clients if c_socket != self.client_socket]


if __name__ == "__main__":
    server = Server(get_ip_address(), 8003)
    server.start()
