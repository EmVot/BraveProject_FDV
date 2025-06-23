import socket
import json

HOST = "127.0.0.1"
PORT = 12345

def send_state(host, port, exposure_value):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        message = {"exposure": exposure_value}
        json_message = json.dumps(message)
        client_socket.sendall(json_message.encode('utf-8'))
        print(f"Messaggio inviato: {json_message}")
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        client_socket.close()



if __name__ == '__main':

    # Esempio di utilizzo
    send_state("127.0.0.1", 12345, 12)
    #creates the TCP socket
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))

    # Start listening for connections
    server_socket.listen(2)
    print(f"Listening on {HOST}:{PORT}...")

    try:
        while True:
            '''
            TODO implement message retrivial logic
            TODO define the signal format
            TODO handle the state transaction (FSM module)
            '''
            # Accept a new connection
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")

            # Receive data
            data = client_socket.recv(1024)
            print(f"Received: {data.decode()}")

            # Optionally, send a response
            client_socket.sendall(b"Message received")

            # Close the connection
            client_socket.close()

    except KeyboardInterrupt:
        print("Shutting down server")

    finally:
        server_socket.close()
