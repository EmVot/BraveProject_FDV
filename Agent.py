import json
import socket
from dataclasses import asdict
from Session import Session, Session1
from UnityMessage import UnityMessage
import time

HOST = "127.0.0.1"
OUT_PORT = 5061
IN_PORT = 5060

END_SIGNAL = "end"


class Agent:
    def __init__(self):
        self.input_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.input_socket.bind((HOST, IN_PORT))
        self.input_socket.listen(1)
        print(f"Listening on {HOST}:{IN_PORT}...")
        self.connection, self.addr = self.input_socket.accept()
        print(f"Connection from {self.addr}")
        print("Connection established, waiting for messages...")
        print("Connecting to Unity...")
        self.output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.output_socket.connect((HOST, OUT_PORT))
        print("Connected to Unity")

    def listen(self):
        try:
            data = self.connection.recv(1024)
            print(f"Received data: {data}")
            data:dict = json.loads(data)
        except Exception as e:
            print(f"Error while listening on agent: {e}")
            self.connection.close()
            data = END_SIGNAL

        return data
    
    def send_state(self, data , message:UnityMessage):
        try:
            if data == END_SIGNAL:
                json_message=json.dumps(data)
            else:
                t_transcript = self.session.get_therapist_transcript(self.step)
                new_d = {
                    "step": self.step,
                    "emotional_state": data.get("emotional_state"),
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
                print(type(data), data)
                if data == END_SIGNAL:
                    print("recieved end signal, shutting down Agent")
                    self.send_state(END_SIGNAL, None)
                    break   
                message =  self.session.map_state((data.get("emotional_state")['valence'], data.get("emotional_state")["arousal"]), self.step)
                self.send_state(data, message)
                self.step += 1
        finally:
            self.input_socket.close()
            self.output_socket.close()



if __name__ == "__main__":
    session_id = "session1"
    Session.register(session_id, Session1)
    agent = Agent()
    agent.launch_session(session_id)
    print("Agent session ended")