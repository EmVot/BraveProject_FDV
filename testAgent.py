import socket
import json


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


# Esempio di utilizzo
send_state("127.0.0.1", 12345, 12)