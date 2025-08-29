import socket
import json
import time
from dataclasses import dataclass, asdict
import numpy as np

HOST = '127.0.0.1'
OUT_PORT = 5060
SCENARIO_STEP = 0.5 #seconds between scenario shift

@dataclass
class EmotionalState:
    '''
    This class describes the emotional state of the patient using its Russel space polar coordinates arousal and valence
    '''
    valence:float
    arousal:float
    
    
    def __init__(self,valence:float, arousal:float):
        self.valence = valence
        self.arousal = arousal
        

    
END_SIGNAL = "end"

def generate_session1_records(tot_steps = 56):
    '''
    This function generates a list of emotional states for the session 1
    '''
    session1_records = [
        EmotionalState(0.7233399911623,-0.6730319357494), #calm
        EmotionalState(-0.31667, 0.26667), #suspicious
        EmotionalState(-0.035, -1/3), #worried
        EmotionalState(-0.075, 0.89833), #alarmed
        EmotionalState(-0.4, 0.78333), #afraid
        EmotionalState(-0.705, 0.55833), #distressed
        EmotionalState(-0.695, 0.59833), #distressed
        EmotionalState(-0.7197157154895,0.6565490462143), #distressed
        EmotionalState(-0.3844066248492,0.8360548493221), #afraid
        EmotionalState(-0.0568380280663,0.8509443309941), #alarmed
        EmotionalState(-0.78333, 0.266667) #bitter
    ]

    if tot_steps > len(session1_records):
        steps_per_segment = tot_steps // (len(session1_records) - 1)
        interpolated_points = []
        for i in range(len(session1_records)-1):
            start_wp = (session1_records[i].valence, session1_records[i].arousal)
            end_wp = (session1_records[i + 1].valence, session1_records[i + 1].arousal)
            
            # Per l'ultimo segmento, includi anche il punto finale
            # Per gli altri segmenti, escludi il punto finale per evitare duplicati
            if i == len(session1_records) - 2:  # ultimo segmento
                t_segment = np.linspace(0, 1, steps_per_segment + 1)[:-1]
                include_end = True
            else:
                t_segment = np.linspace(0, 1, steps_per_segment + 1)[:-1]  # escludi ultimo punto
                include_end = False
            
            # Interpolazione lineare semplice per ogni segmento
            x_segment = start_wp[0] + t_segment * (end_wp[0] - start_wp[0])
            y_segment = start_wp[1] + t_segment * (end_wp[1] - start_wp[1])

            #interpolated_points.append(EmotionalState(start_wp[0], start_wp[1]))
            interpolated_points.extend([EmotionalState(x, y) for x, y in zip(x_segment, y_segment)])

            if include_end:
               interpolated_points.append(EmotionalState(end_wp[0], end_wp[1]))

        session1_records = interpolated_points
    
    print(f"Generated {len(session1_records)} states for session 1")
    
    return session1_records


def send_state(client_socket, patient_transcript: str, emotional_state:EmotionalState = EmotionalState(0,0), end = False):
    try:
        if end:
            json_message=json.dumps(END_SIGNAL)
        else:
            full_state = {"patient_transcript": patient_transcript, "emotional_state": asdict(emotional_state)}
            json_message = json.dumps(full_state)
        client_socket.sendall(json_message.encode('utf-8'))

    except Exception as e:
        print(f"Errore: {e}")
        client_socket.close()
        exit(-1)


if __name__ == '__main__':
    states = generate_session1_records(tot_steps=55)
    #   initial state
    print("Begin")
    print(len(states), states)
    with open('patient_transcripts.txt', 'r') as f:
       patient_transcripts = f.readlines()
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, OUT_PORT))
    except Exception as e:
        print(f"Errore: {e}")
        client_socket.close()
        exit(-1)
    for i in range(len(states)):
        print(f"Sending state {i}")
        send_state(client_socket, patient_transcript=patient_transcripts[i], emotional_state=states[i])
        time.sleep(SCENARIO_STEP)
    send_state(client_socket, patient_transcript=None, emotional_state=None, end=True)
    
    print("End")