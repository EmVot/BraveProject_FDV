import socket
import json

HOST = "127.0.0.1"
IN_PORT = 5061
END_SIGNAL = "end"

if __name__ == "__main__":
    end_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    end_socket.bind((HOST, IN_PORT))
    end_socket.listen(1)
    connection, addr = end_socket.accept()
    print(f"Connection from {addr}")
    data_dict = {}
    while True:
       try:
           data:dict = json.loads(connection.recv(1024))
           print(f"End received data: {data}")  
           if data == END_SIGNAL:
               print("recieved end signal, shutting down")
               break
           data_dict[data.get('step')] = {"emotional_state": data.get('emotional_state'),
                                          "patient_transcript": data.get('patient_transcript'),
                                          "therapist_transcript": data.get('therapist_transcript'),
                                           "unity_message": data.get('unity_message')}
       except Exception as e:
           print(f"Error while listening on end: {e}")
           connection.close()
           end_socket.close()
           break
    with open('session1_data.json', 'w') as f:
        json.dump(data_dict, f, indent=4)
    print("End data saved to session1_data.json")
 

