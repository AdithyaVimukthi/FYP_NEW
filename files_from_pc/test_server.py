import cv2
import socket
import struct
import pickle


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return "Error: " + str(e)


cap = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((get_ip_address(), 8485))  # replace with your host and port
sock.listen(10)
print(f'Server listening... on {get_ip_address()}')
conn, addr = sock.accept()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Serialize frame
    data = pickle.dumps(frame)

    # Send message length first
    message_size = struct.pack(">L", len(data))

    # Then data
    conn.sendall(message_size + data)

cap.release()
