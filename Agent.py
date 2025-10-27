import json
import socket
import time
import math

from dataclasses import asdict
from websocket import create_connection, WebSocketConnectionClosedException
from Session import Session, Session1
from UnityState import UnityState

HOST = "127.0.0.1"
UNITY_WS_PORT = 8080   # server WS di Unity
IN_PORT = 5060         # input TCP come già avevi

END_SIGNAL = "end"

# Parametri del pannello (per scegliere l'action corretta)
SLIDER_PARAMS = {"exposure", "rain", "turbolence"}
TOGGLE_OR_OPTION_PARAMS = {"flash", "rumbling", "oxygenMasks", "voices"}


class Agent:
    def __init__(self):
        # --- PREPARA code/variabili PRIMA di connetterti ---
        self.ws = None
        self.ws_url = f"ws://{HOST}:{UNITY_WS_PORT}/"
        self.outgoing_queue = []      # <-- CREA QUI
        self.state_history = {}       # <-- (facoltativo ma logico metterla qui)

        # --- WebSocket client verso Unity, con retry ---
        self._ws_connect_with_retry()

        # --- Socket TCP di input (come avevi già) ---
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.input_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.input_socket.bind((HOST, IN_PORT))
        self.input_socket.listen(1)
        print(f"Listening on {HOST}:{IN_PORT}...")
        #self.connection, self.addr = self.input_socket.accept()
        #print(f"Connection from {self.addr}")
        #print("Connection established, waiting for messages...")
        # self.output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.output_socket.connect((HOST, OUT_PORT))
        # print("Connected to Unity")

    # ---------- Connessione/reconnessione WS ----------

    def _ws_connect_with_retry(self, max_backoff=5.0):
        """Prova a connettersi a Unity in loop (backoff fino a 5s)."""
        delay = 0.5
        while True:
            try:
                print(f"Connecting to Unity WS at {self.ws_url} ...")
                self.ws = create_connection(self.ws_url, timeout=5)
                self.ws.settimeout(1.0)  # breve timeout per ping/read
                print("✅ Connected to Unity WebSocket")
                # svuota coda se c’è
                self._flush_queue()
                return
            except Exception as e:
                print(f"❌ Unity WS not available yet: {e} — retrying in {delay:.1f}s")
                time.sleep(delay)
                delay = min(max_backoff, delay * 1.5)

    def _ws_safe_send(self, payload: dict):
        """Invia un messaggio; se WS è chiuso, prova a riconnettere e accoda."""
        msg = json.dumps(payload)
        try:
            if self.ws is None:
                raise WebSocketConnectionClosedException("WS not connected")
            self.ws.send(msg)
            print(f"📤 Sent WS message: {payload}")
        except Exception as e:
            print(f"⚠️ WS send failed: {e}. Queuing and reconnecting...")
            self.outgoing_queue.append(msg)
            self._ws_reconnect()

    def _ws_reconnect(self):
        try:
            if self.ws:
                try:
                    self.ws.close()
                except Exception:
                    pass
            self._ws_connect_with_retry()
        except Exception as e:
            print(f"❌ Reconnect failed: {e}")

    def _flush_queue(self):
        """Invia tutto ciò che è in coda dopo una riconnessione."""
        if not self.outgoing_queue or self.ws is None:
            return
        print(f"🔁 Flushing {len(self.outgoing_queue)} queued messages...")
        while self.outgoing_queue:
            msg = self.outgoing_queue.pop(0)
            try:
                self.ws.send(msg)
                print(f"📤 Sent queued: {msg}")
            except Exception as e:
                print(f"⚠️ Failed while flushing queue: {e}")
                # Rimetti in testa e tenta una nuova reconnect
                self.outgoing_queue.insert(0, msg)
                self._ws_reconnect()
                break

    # ---------- Logica di sessione ----------

    def listen(self):
        try:
            data = self.connection.recv(4096)
            if not data:
                raise ConnectionError("TCP input socket closed")
            return json.loads(data)
        except Exception as e:
            print(f"Error while listening on agent: {e}")
            try:
                self.connection.close()
            except Exception:
                pass
            return END_SIGNAL

    def save_state(self, data, state):
        t_transcript = self.session.get_therapist_transcript(self.step)
        new_s = {
            "emotional_state": data.get("emotional_state"),
            "patient_transcript": data.get("patient_transcript"),
            "therapist_transcript": t_transcript,
            "unity_state": asdict(state)
        }
        self.state_history[str(self.step)] = new_s

    def _build_command(self, param, value):
        # Slider → update_param con numerico
        if param in SLIDER_PARAMS:
            try:
                value = float(value)
            except (TypeError, ValueError):
                pass
            return {"type": "command", "action": "update_param", "param": param, "value": value}
        # Toggle/Option → toggle_param con bool/string
        elif param in TOGGLE_OR_OPTION_PARAMS:
            return {"type": "command", "action": "toggle_param", "param": param, "value": value}
        else:
            return {"type": "command", "action": "update_sliders", "param": param, "value": value}

    def send_to_unity(self, param, value):
        payload = self._build_command(param, value)
        self._ws_safe_send(payload)

    def save_json_history(self, session_id):
        with open(f'session_{session_id}.json', 'w', encoding='utf-8') as f:
            json.dump(self.state_history, f, indent=4, ensure_ascii=False)
        print(f"End data saved to session_{session_id}.json")

    def launch_session(self, session_id):
        self.session = Session(session_id)
        self.step = 0
        try:
            while True:
                data = self.listen()
                print(self.step)
                if data == END_SIGNAL:
                    print("received end signal, shutting down Agent")
                    # opzionale: notifica di fine
                    self._ws_safe_send({"type": "command", "action": "toggle_param", "param": "msg", "value": END_SIGNAL})
                    break

                # La Session deve restituire: message: dict {param: value}, state: dataclass
                message, state = self.session.map_state(
                    (data.get("emotional_state")["valence"], data.get("emotional_state")["arousal"]),
                    self.step
                )
                slider_heights = calcola_altezze_slider((data.get("emotional_state")["valence"], data.get("emotional_state")["arousal"]))
                message['sliders'] = slider_heights
                print("mapped message:", message)
                self.save_state(data, state)


                for key, value in message.items():
                    self.send_to_unity(key, value)

                self.step += 1
        finally:
            self.save_json_history(session_id)
            self.input_socket.close()
            self.output_socket.close()
            #self.ws.close()

    def execute_json_session(self, session_file):
        print("Si apre?????")
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        unity_state = UnityState()
        print(f"Session data: {session_data}")
        for step, state in session_data.items():
            print(f"Step: {step}, State: {state}")
            for key, value in state['unity_state'].items():
                if getattr(unity_state, key) != value:
                    self.send_to_unity(key, value)
                    setattr(unity_state, key, value)
            time.sleep(1) 


def calcola_altezze_slider(punto):
    
    riferimenti = {
        'ANGER': (-0.9, 0.2),
        'FEAR': (-0.4,0.78333),
        'CALM': (0.7233399911623,-0.6730319357494)
    }
    
    distanze = {}
    for emozione, ref_punto in riferimenti.items():
        distanza = math.sqrt((punto[0] - ref_punto[0])**2 + (punto[1] - ref_punto[1])**2)
        distanze[emozione] = distanza
    
    
    altezze = {}
    for emozione, distanza in distanze.items():
        altezza_percentuale = max(0, min(100, (1 - distanza / 2) * 100))
        altezze[emozione] = round(altezza_percentuale, 2)
    
    return altezze

if __name__ == "__main__":
    session_id = "session1"
    Session.register(session_id, Session1)
    agent = Agent()
    # agent.launch_session(session_id)
    print("Agent session ended")
    agent.execute_json_session('synthetic_session/synthetic_session_30.json')