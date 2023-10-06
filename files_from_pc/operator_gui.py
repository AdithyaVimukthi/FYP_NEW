import socket
import cv2
import pickle
import struct
import imutils
import tkinter as tk
from tkinter import simpledialog

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

    def video_receive(self):
        while len(self.data) < self.payload_size:
            packet = self.client_socket.recv(4 * 1024)  # 4K
            if not packet:
                break
            self.data += packet

        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(self.data) < msg_size:
            self.data += self.client_socket.recv(4 * 1024)

        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        frame = pickle.loads(frame_data)

        return frame

class LoginDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Server IP:").grid(row=0)
        tk.Label(master, text="Server Port:").grid(row=1)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1  # initial focus

    def apply(self):
        self.server_ip = self.e1.get()
        self.server_port = int(self.e2.get())

if __name__ == "__main__":
    ROOT = tk.Tk()
    ROOT.withdraw()
    # The input dialog
    login = LoginDialog(ROOT)
    SERVER_IP = login.server_ip
    SERVER_PORT = login.server_port

    client = Client(SERVER_IP, SERVER_PORT)
    client.connect()

    while True:
        frame = client.video_receive()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        cv2.imshow('TRANSMITTING VIDEO', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            message = "quit"

        if message.lower() == "quit":
            client.disconnect()
            break

        client.send_message(message)