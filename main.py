from BraveProject_FDV.Session import Session, Session1
from BraveProject_FDV.Agent import Agent, HOST, OUT_PORT, END_SIGNAL
import socket
import json


if __name__ == "__main__":
    Session.register("session1", Session1)
    agent = Agent()
    agent.launch_session("session1")
    #open socket at port 5000 to receive messages from agent
    end_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    end_socket.connect((HOST, OUT_PORT))
    data_dict = {}
    while True:
       try:
           client_socket, addr = end_socket.accept()
           print(f"Connection from {addr}")
           data:dict = json.loads(client_socket.recv(1024))
           if data.get('message') == END_SIGNAL:
               print("recieved end signal, shutting down")
               break
           data_dict[data.get('step')] = {"emotional_state": data.get('emotional_state'),
                                          "patient_transcript": data.get('patient_transcript'),
                                          "therapist_transcript": data.get('therapist_transcript'),
                                           "unity_message": data.get('unity_message')}
       except Exception as e:
           print(f"Error while listening message: {e}")
           client_socket.close()
           end_socket.close()
           break
    with open('session1_data.json', 'w') as f:
        json.dump(data_dict, f, indent=4)
 

