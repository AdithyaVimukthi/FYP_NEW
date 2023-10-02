import socket
import cv2
import pickle
import struct
import imutils


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = b""
        self.payload_size = struct.calcsize("Q")

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server {self.host}:{self.port}")

    def send_message(self, message):
        self.client_socket.send(message.encode())

    def disconnect(self):
        self.client_socket.send("disconnect".encode())
        self.client_socket.close()
        print("Disconnected from server")


# if __name__ == "__main__":
#     client = Client("192.168.1.5", 8005)  # Replace with the server's IP and port
#     client.connect()
#
#     while True:
#         message = input("Enter a message (type 'quit' to exit): ")
#         if message.lower() == "quit":
#             client.disconnect()
#             break
#
#         client.send_message(message)
