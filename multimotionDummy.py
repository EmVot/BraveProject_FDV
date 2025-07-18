from re import A
import socket
import json
import time
from dataclasses import dataclass, asdict
from tracemalloc import start
from flask import session
import numpy as np

HOST = "127.0.0.1"
OUT_PORT = 5001
SCENARIO_STEP = 5 #seconds between scenario shift

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
        

    
END_SIGNAL = {
    "message":"end"
}

def generate_session1_records(tot_steps = 50):
    '''
    This function generates a list of emotional states for the session 1
    '''
    session1_records = [
        EmotionalState(0.7233399911623,-0.6730319357494),
        EmotionalState(-0.31667, 0.26667),
        EmotionalState(-0.035, -1/3),
        EmotionalState(-0.075, 0.89833),
        EmotionalState(-0.4, 0.78333),
        EmotionalState(-0.705, 0.55833),
        EmotionalState(-0.695, 0.59833), #start loosening fearful variables
        EmotionalState(-0.075, 0.87833),
        EmotionalState(-0.78333, 0.266667),
        EmotionalState(-0.035, -0.36)
    ]

    if tot_steps > len(session1_records):
        steps_per_segment = tot_steps // (len(session1_records) - 1)
        interpolated_points = []
        for i in range(len(session1_records)-1):
            start_wp = (session1_records[i].arousal, session1_records[i].valence)
            end_wp = (session1_records[i + 1].arousal, session1_records[i + 1].valence)
            
            # Per l'ultimo segmento, includi anche il punto finale
            # Per gli altri segmenti, escludi il punto finale per evitare duplicati
            if i == len(session1_records) - 2:  # ultimo segmento
                t_segment = np.linspace(0, 1, steps_per_segment + 1)
                include_end = True
            else:
                t_segment = np.linspace(0, 1, steps_per_segment + 1)[:-1]  # escludi ultimo punto
                include_end = False
            
            # Interpolazione lineare semplice per ogni segmento
            x_segment = start_wp[0] + t_segment * (end_wp[0] - start_wp[0])
            y_segment = start_wp[1] + t_segment * (end_wp[1] - start_wp[1])

            interpolated_points.append(EmotionalState(start_wp[0], start_wp[1]))
            interpolated_points.extend([EmotionalState(x, y) for x, y in zip(x_segment, y_segment)])

            if include_end:
               interpolated_points.append(EmotionalState(end_wp[0], end_wp[1]))

        session1_records = interpolated_points
    
    return session1_records


def send_state(host, port, patient_transcript: str, emotional_state:EmotionalState = EmotionalState(0,0), end = False):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))

        if end:
            json_message=json.dumps(END_SIGNAL)
        else:
            full_state = {"patient_transcript": patient_transcript, "state": asdict(emotional_state)}
            json_message = json.dumps(full_state)

        client_socket.sendall(json_message.encode('utf-8'))
        print(f"Messaggio inviato: {json_message}")

    except Exception as e:
        print(f"Errore: {e}")
        client_socket.close()
        exit(-1)
    finally:
        client_socket.close()


if __name__ == '__main__':
    states = generate_session1_records(tot_steps=50)
    #   initial state
    print("Begin")
    with open('patient_transcript.txt', 'r') as f:
       patient_transcripts = f.readlines()

    for i in len(states):
        send_state(HOST,OUT_PORT, patient_transcript=patient_transcripts[i], emotional_state=states[i])
        time.sleep(SCENARIO_STEP)
    send_state(HOST,OUT_PORT,end=True)
    
    print("End")
    #




    # ##   emotional state = relaxed
    # send_state(HOST,OUT_PORT,EmotionalState(0.8003965398535,-0.6310763224595))
    # time.sleep(SCENARIO_STEP)

    # # starting to distress the patient
    # ## emotional state: suspicious
    # send_state(HOST, OUT_PORT, EmotionalState(0.413991411612474, 139.89909245378777))
    # time.sleep(SCENARIO_STEP)

    # ## emotional state: worried
    # send_state(HOST, OUT_PORT, EmotionalState(0.3416666666666667, -102.68038349181982))
    # time.sleep(SCENARIO_STEP)

    # ## emotional state: alarmed
    # send_state(HOST, OUT_PORT, EmotionalState(0.9014586944379525, 94.7724388316847))
    # time.sleep(SCENARIO_STEP)

    # # patient fully scared
    # ## emotional state: scared
    # send_state(HOST, OUT_PORT, EmotionalState(0.9204467514322717, 121.67546873810922))
    # time.sleep(SCENARIO_STEP)

    # ## emotional state: distressed
    # send_state(HOST, OUT_PORT, EmotionalState(0.8993114650170492, 141.6221079228427)) #start loosening fearful variables
    # time.sleep(SCENARIO_STEP)

    # # patient emotions begin to ease
    # ## emotional state: alarmed
    # send_state(HOST, OUT_PORT, EmotionalState(0.9014586944379525, 94.7724388316847))
    # time.sleep(SCENARIO_STEP)

    # ## emotional state: bitter
    # send_state(HOST, OUT_PORT, EmotionalState(0.8274794391537607, 161.20011484134733))
    # time.sleep(SCENARIO_STEP)

    # ## emotional state: worried
    # send_state(HOST, OUT_PORT, EmotionalState(0.3416666666666667, -102.68038349181982))
    # time.sleep(SCENARIO_STEP)