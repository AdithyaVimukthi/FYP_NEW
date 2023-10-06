import sys
import socket
import threading
import pickle
import struct
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from servo import servo_controller
from camera import camera

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
    def __init__(self, port):
        self.cam = camera()
        self.cap = None
        self.host = get_ip_address()
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.disconnect_msg = 'disconnect'

    def accept_connection(self):
        print("Server Start...............")
        print(f"Server ip => {self.host}")
        print(f"Server Port => {self.port}")
        while True:
            conn, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        print(f"Connected to {addr}")
        
        try:
            self.video_send(conn)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()
            print(f"Disconnected from {addr}")

    def video_send(self, conn):
        while True:
            frame = self.cam.capture() # RGB frame
            # ret, frame = self.cap.read()
            data = pickle.dumps(frame)
            message_size = struct.pack("Q", len(data))
            conn.sendall(message_size + data)

            try:
                message = conn.recv(1024)
                if message:
                    return message.decode()
                    # print(message.decode())
            except:
                pass

if __name__ == "__main__":
    server = Server(8007)  # Replace with your IP and port
    server.accept_connection()