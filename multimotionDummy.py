import socket
import json
import time

HOST = "127.0.0.1"
OUT_PORT = 5000
SCENARIO_STEP = 30 #seconds between scenario shift

class EmotionalState:
    '''
    This class describes the emotional state of the patient using its Russel space polar coordinates arousal and valence
    '''

    arousal:float
    valence:float
    
    def __init__(self,arousal:float,valence:float):
        self.arousal = arousal
        self.valence = valence
    
    def json(self):
        '''
        This method returns the Emotional state in json format
        '''
        return f'''arousal:{self.arousal},valence:{self.valence}'''


def send_state(host, port, emotional_state:EmotionalState):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        message = emotional_state.json()
        json_message = json.dumps(message)
        client_socket.sendall(json_message.encode('utf-8'))
        print(f"Messaggio inviato: {json_message}")

    except Exception as e:
        print(f"Errore: {e}")

    finally:
        client_socket.close()


if __name__ == '__main':


    #   initial state
    ##   emotional state = relaxed
    send_state(HOST,OUT_PORT,EmotionalState(0.8003965398535,-0.6310763224595))
    time.sleep(SCENARIO_STEP)

