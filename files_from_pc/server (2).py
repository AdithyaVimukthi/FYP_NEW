# TCP_SERVER.py
import socket
import cv2
import pickle
import struct
import threading


class Server:
    def __init__(self, host, port):
        self.cap = None
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

    def accept_connection(self):
        while True:
            conn, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        print(f"Connected to {addr}")
        self.cap = cv2.VideoCapture(0)  # 0 for webcam
        try:
            self.video_send(conn)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.cap.release()
            conn.close()
            print(f"Disconnected from {addr}")

    def video_send(self, conn):
        while True:
            ret, frame = self.cap.read()
            data = pickle.dumps(frame)
            message_size = struct.pack("Q", len(data))
            conn.sendall(message_size + data)

            try:
                message = conn.recv(1024)
                if message:
                    print(message.decode())
            except:
                pass


if __name__ == "__main__":
    server = Server("192.168.1.4", 8003)  # Replace with your IP and port
    server.accept_connection()
