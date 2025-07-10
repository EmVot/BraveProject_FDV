import socket
import json

HOST = "127.0.0.1"
OUT_PORT = 5000
IN_PORT = 5001


lightining_json = {
    'lightinigs':bool
}

exposure_json = {
    'min':float,
    'max':float,
    'exposure':float
}

rain_json = {
    'min' : 0.0,
    'max' : 2e4,
    'rain':float
}

flashes_json = {
    'flashes':bool
}

turbolences_json = {
    'min':0.0,
    'max':2.0,
    'pace': .1,
    'turbolescences':float
}

voices_json = {
    'voice':{
        'voice1':1,
        'voice2':2,
        'voice3':3,
    },
    'volume':{
        'intensity':float,
        'min':0.0,
        'max':1.0,
        'step':.1
    }
}

oxmasks_json = {
    'masks': bool
}

rumbling_json = {
    'rumbling':bool
}


END_SIGNAL = "end"


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



if __name__ == '__main__':

    # Esempio di utilizzo
    ## send_state("127.0.0.1", 12345, 12)
    #creates the TCP socket for input signaling
    input_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # Bind the socket to the address and port
    input_socket.bind((HOST, IN_PORT))

    # Start listening for connections
    input_socket.listen(2)
    print(f"Listening on {HOST}:{IN_PORT}...")
    

    try:
        while True:
            '''
            TODO implement message retrivial logic
            TODO define the signal format
            TODO handle the state transaction (FSM module)
            '''
            # Accept a new connection
            client_socket, addr = input_socket.accept()
            print(f"Connection from {addr}")

            # Receive data
            data:dict = json.loads(client_socket.recv(1024))
            #print(f"Received: {data}")

            if data.get('message') == END_SIGNAL:
                print("recived end signal, shutting down AI Agent")
                break

            # Close the connection
            client_socket.close()

    except KeyboardInterrupt:
        print("Shutting down server")

    finally:
        input_socket.close()
