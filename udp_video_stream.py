import pickle
import socket
import struct

import cv2

host = '127.0.0.1'
port = 8083
payload_size = struct.calcsize("L")

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
socket.bind((host, port))
socket.listen(10)

connection, address = socket.accept()


def render_frame():
    data = b''
    while True:
        if connection is not None:
            while len(data) < payload_size:
                data += connection.recv(4096)
            packed_msg_size = data[:payload_size]

            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += connection.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data)
            cv2.imshow(str(address), frame)
            cv2.waitKey(10)
            send_frame()
        else:
            send_frame()


def send_frame():
    current_frame = cv2.VideoCapture(0)
    while True:
        try:
            ret, frame = current_frame.read()
            data = pickle.dumps(frame)
            socket.sendall(struct.pack("L", len(data)) + data)
        except Exception as e:
            socket.close()
            print("Error" + str(e))
            exit(1)


if __name__ == '__main__':
    render_frame()
    socket.close()
