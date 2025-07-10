import socket
import json
import time
from dataclasses import dataclass, asdict

HOST = "127.0.0.1"
OUT_PORT = 5001
SCENARIO_STEP = 5 #seconds between scenario shift

@dataclass
class EmotionalState:
    '''
    This class describes the emotional state of the patient using its Russel space polar coordinates arousal and valence
    '''

    arousal:float
    valence:float
    
    def __init__(self,arousal:float,valence:float):
        self.arousal = arousal
        self.valence = valence

    
END_SIGNAL = {
    "message":"end"
}


def send_state(host, port, emotional_state:EmotionalState = EmotionalState(0,0), end = False):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))

        if end:
            json_message=json.dumps(END_SIGNAL)
        else:
            json_message = json.dumps(asdict(emotional_state))

        client_socket.sendall(json_message.encode('utf-8'))
        print(f"Messaggio inviato: {json_message}")

    except Exception as e:
        print(f"Errore: {e}")
        client_socket.close()
        exit(-1)


    finally:
        client_socket.close()


if __name__ == '__main__':

    #   initial state
    print("Begin")

    ##   emotional state = relaxed
    send_state(HOST,OUT_PORT,EmotionalState(0.8003965398535,-0.6310763224595))
    time.sleep(SCENARIO_STEP)

    # starting to distress the patient
    ## emotional state: suspicious
    send_state(HOST, OUT_PORT, EmotionalState(0.413991411612474, 139.89909245378777))
    time.sleep(SCENARIO_STEP)

    ## emotional state: worried
    send_state(HOST, OUT_PORT, EmotionalState(0.3416666666666667, -102.68038349181982))
    time.sleep(SCENARIO_STEP)

    ## emotional state: alarmed
    send_state(HOST, OUT_PORT, EmotionalState(0.9014586944379525, 94.7724388316847))
    time.sleep(SCENARIO_STEP)

    # patient fully scared
    ## emotional state: scared
    send_state(HOST, OUT_PORT, EmotionalState(0.9204467514322717, 121.67546873810922))
    time.sleep(SCENARIO_STEP)

    ## emotional state: distressed
    send_state(HOST, OUT_PORT, EmotionalState(0.8993114650170492, 141.6221079228427)) #start loosening fearful variables
    time.sleep(SCENARIO_STEP)

    # patient emotions begin to ease
    ## emotional state: alarmed
    send_state(HOST, OUT_PORT, EmotionalState(0.9014586944379525, 94.7724388316847))
    time.sleep(SCENARIO_STEP)

    ## emotional state: bitter
    send_state(HOST, OUT_PORT, EmotionalState(0.8274794391537607, 161.20011484134733))
    time.sleep(SCENARIO_STEP)

    ## emotional state: worried
    send_state(HOST, OUT_PORT, EmotionalState(0.3416666666666667, -102.68038349181982))
    time.sleep(SCENARIO_STEP)

    send_state(HOST,OUT_PORT,end=True)
    
    print("End")
    #

