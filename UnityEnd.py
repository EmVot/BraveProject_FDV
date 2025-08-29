import socket
import json

HOST = "127.0.0.1"
IN_PORT = 5061
END_SIGNAL = {"msg" : "end"}

if __name__ == "__main__":
    end_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    end_socket.bind((HOST, IN_PORT))
    end_socket.listen(1)
    connection, addr = end_socket.accept()
    print(f"Connection from {addr}")
    data_dict = {}
    end = False
    while not end:
        try:
            data = connection.recv(4096).decode()
            print(f"Received buffer: {data}")
            decoder = json.JSONDecoder()
            idx = 0
            while idx < len(data):
                obj, idx = decoder.raw_decode(data, idx)
                print(obj)
                if obj == END_SIGNAL:
                    print("recieved end signal, shutting down")
                    end = True
        except Exception as e:
           print(f"Error while listening on end: {e}")
           connection.close()
           end_socket.close()
           break
    connection.close()
    end_socket.close()
 

