import json
import socket
from dataclasses import asdict
from Session import Session, Session1
import time

from websocket import create_connection

HOST = "127.0.0.1"
OUT_PORT = 8080
IN_PORT = 5060

END_SIGNAL = "end"


class Agent:
    def __init__(self):
        print("Connecting to Unity (WebSocket)...")
        self.ws = create_connection(f"ws://{HOST}:{OUT_PORT}/")   # <-- WebSocket, non TCP
        print("Connected to Unity (WebSocket)")

        self.input_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.input_socket.bind((HOST, IN_PORT))
        self.input_socket.listen(1)
        print(f"Listening on {HOST}:{IN_PORT}...")
        self.connection, self.addr = self.input_socket.accept()
        print(f"Connection from {self.addr}")
        print("Connection established, waiting for messages...")
        #self.output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.output_socket.connect((HOST, OUT_PORT))
        #print("Connected to Unity")

        self.state_history = {}

    def listen(self):
        try:
            data = self.connection.recv(1024)
            #print(f"Received data: {data}")
            data:dict = json.loads(data)
        except Exception as e:
            print(f"Error while listening on agent: {e}")
            self.connection.close()
            data = END_SIGNAL

        return data
    
    def save_state(self, data , state):
        t_transcript = self.session.get_therapist_transcript(self.step)
        new_s = {
            "emotional_state": data.get("emotional_state"),
            "patient_transcript": data.get("patient_transcript"),
            "therapist_transcript": t_transcript,
            "unity_state": asdict(state)
        }
        self.state_history[f"{self.step}"] = new_s

    def _to_unity_value(self, v):
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, (int, float)):
            return format(v, "g")  # punto decimale, cultura invariante
        return str(v)

    def send_unity_message(self, msg):
        try:
            v = self._to_unity_value(list(msg.values())[0])
            k = list(msg.keys())[0]
            self.ws.send(json.dumps({k: v}))
            #json_message = json.dumps(msg)
            #self.output_socket.sendall(json_message.encode('utf-8'))
            #print(f"Sent message: {json_message}")
            print(f"Sent WS message: {msg}")
        except Exception as e:
            print(f"Error while sending message: {e}")
            #self.output_socket.close()
            self.ws.close()

    def save_json_history(self, session_id):
        with open(f'session_{session_id}.json', 'w') as f:
            json.dump(self.state_history, f, indent=4)
        print(f"End data saved to session_{session_id}.json")

    def launch_session(self, session_id):
        self.session = Session(session_id)
        self.step = 0
        try:
            while True:
                data = self.listen()
                print(self.step)
                if data == END_SIGNAL:
                    print("recieved end signal, shutting down Agent")
                    self.send_unity_message({"msg" : END_SIGNAL})
                    break   
                message, state =  self.session.map_state((data.get("emotional_state")['valence'], data.get("emotional_state")["arousal"]), self.step)
                print(message)
                self.save_state(data, state)
                for key, value in message.items():
                    self.send_unity_message({key: value})
                self.step += 1
        finally:
            self.save_json_history(session_id)
            self.input_socket.close()
            #self.output_socket.close()
            self.ws.close()

if __name__ == "__main__":
    session_id = "session1"
    Session.register(session_id, Session1)
    agent = Agent()
    agent.launch_session(session_id)
    print("Agent session ended")