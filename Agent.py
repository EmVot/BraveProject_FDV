import json
import socket
from dataclasses import asdict

from regex import E

from BraveProject_FDV.multimotionDummy import EmotionalState
from Session import Session
from UnityMessage import UnityMessage

HOST = "127.0.0.1"
OUT_PORT = 5000
IN_PORT = 5001

END_SIGNAL = {
    "message":"end"
}

class Agent:
    def __init__(self):
        self.input_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.input_socket.bind((HOST, IN_PORT))
        self.input_socket.listen(2)
        print(f"Listening on {HOST}:{IN_PORT}...")
        self.output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.output_socket.connect((HOST, OUT_PORT))

    def listen(self):
        try:
            client_socket, addr = self.input_socket.accept()
            print(f"Connection from {addr}")
            data:dict = json.loads(client_socket.recv(1024))
        except Exception as e:
            print(f"Error while listening message: {e}")
            client_socket.close()
            data = json.dumps(END_SIGNAL)

        return data
    
    def send_state(self, data , message:UnityMessage):
        try:
            t_transcript = self.session.get_therapist_transcript(self.step)
            new_d = {
                "step": self.step,
                "emotional_state": asdict(data.get("emotional_state")),
                "patient_transcript": data.get("patient_transcript"),
                "therapist_transcript": t_transcript,
                "unity_message": asdict(message)
            }
            json_message = json.dumps(new_d)
            self.output_socket.sendall(json_message.encode('utf-8'))
            print(f"Sent message: {json_message}")
        except Exception as e:
            print(f"Error while sending message: {e}")
            self.output_socket.close()
    
    def launch_session(self, session_id):
        self.session = Session(session_id)
        self.step = 0
        try:
            while True:
                data = self.listen()
                if data.get('message') == END_SIGNAL:
                    print("recieved end signal, shutting down Agent")
                    self.send_state(END_SIGNAL)
                    break
                self.step += 1   
                message =  self.session.map_state(data.get("emotional_state"), self.step)

                self.send_state(data, message)
        finally:
            self.input_socket.close()
            self.output_socket.close()



    ### NB ogni messaggio mandato a unity implpementare un tempo di attesa per la stabilizzazione del prossimo stato emotivo