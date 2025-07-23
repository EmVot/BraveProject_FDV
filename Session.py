import math
from abc import ABC, abstractmethod

from UnityMessage import UnityMessage
from multimotionDummy import EmotionalState


class Session(ABC):
    _sessions = {}
    
    def __new__(cls, session_id, tau=0):
        if cls is not Session: 
            instance = super().__new__(cls)
            instance.tau = tau
            return instance
        
        if session_id in cls._sessions:
            session_class = cls._sessions[session_id]
            instance = session_class.__new__(session_class, session_id, tau)
            return instance
        raise ValueError(f"Session {session_id} not found")
    
    def __init__(self, session_id, tau=1.0):
        pass

    @classmethod
    def register(cls, session_id, session_class):
        cls._sessions[session_id] = session_class
    
    @abstractmethod
    def map_state(self, state: EmotionalState, step: int) -> UnityMessage:
        pass
    
    def define_references(self, dict_ref):
        self.dict_ref = dict_ref

    def is_within_radius(self, point1, point2):
        x1, y1 = point1
        r2, theta2 = point2
        
        
        x2, y2 = r2 * math.cos(theta2), r2 * math.sin(theta2)
        
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        return distance <= self.tau

class Session1(Session):
    def __init__(self, session_id, tau=0,tot_steps=50):
        super().__init__(session_id, tau)
        self.tot_steps = tot_steps
        self.tau = tau
        self._unity_state = UnityMessage(
                    rain = 0.0,
                    lightings = False,
                    exposure = 8.0,
                    oxMasks = False,
                    turbolences = 0.0,
                    voices = {"volume":0.5,'type':0},
                    rumbling = True,
                    seatbelt_signal = False,
                    blinking_lights = False,
                    applauses = False
        )
        self.ref_points = [
            (0.5723106166247,-0.8365047036457), # calm - 0
            (0.413991411612474, 139.89909245378777), #suspicious - 1
            (0.3416666666666667, -102.68038349181982), # worried - 2
            (0.9014586944379525, 94.7724388316847), #alarmed - 3
            (0.9204467514322717, 121.67546873810922), # afraid - 4
            (0.8993114650170492, 141.6221079228427), # distressed - 5
            (0.8274794391537607, 161.20011484134733),  #bitter- 6
        ]
        with open('therapist_transcripts.txt', 'r') as file:
            self.therapist_transcripts = file.readlines()
            
    def get_therapist_transcript(self, step):
        return self.therapist_transcripts[step]
    
    def map_state(self, state, step) -> UnityMessage:
        closest_index = next(
                (i for i, point in enumerate(self.ref_points) if self.is_within_radius(state, point)),
                -1
            )
        match closest_index:
            case 0 if step < self.tot_steps / 10: # 1
                self._unity_state.exposure = self._unity_state.exposure - 0.3 * self._unity_state.exposure
                self._unity_state.voices = {'volume' : 0.8, 'type' : 0}
                self._unity_state.rumbling = True
                return self._unity_state
            case 1 if step < self.tot_steps / 10: #2
                self._unity_state.exposure = self._unity_state.exposure - 0.5 * self._unity_state.exposure
                self._unity_state.rain = 200
                self._unity_state.voices = {'volume' : 1, 'type' : 0}
                return self._unity_state
            case 2 if step < self.tot_steps / 15: #3
                self._unity_state.exposure = self._unity_state.exposure - 0.5 * self._unity_state.exposure
                self._unity_state.rain = 10000
                self._unity_state.voices = {'volume' : 1, 'type' : 2}
                return self._unity_state
            case 2: #10
                self._unity_state.exposure += self._unity_state.exposure * 0.3
                self._unity_state.voices = {'volume' : 1, 'type' : 0}
                return self._unity_state
            case 3 if step < self.tot_steps / 20: #4
                self._unity_state.lightings = True
                self._unity_state.rain = 20000
                self._unity_state.voices = {'volume' : 1, 'type' : 2}
                self._unity_state.seatbelt_signal = True
                return self._unity_state
            case 3: #8
                self._unity_state.oxMasks=False
                self._unity_state.exposure += self._unity_state.exposure * 0.3
                self._unity_state.voices={'volume':0.5, 'type':2}
                self._unity_state.rain = 0
                return self._unity_state
            case 4 if step < self.tot_steps / 25: #5
                self._unity_state.oxMasks = True
                self._unity_state.voices = {'volume' : 1, 'type' : 3}
                self._unity_state.turbolences = 1.5
                return self._unity_state
            case 5 if step < self.tot_steps / 30: #6
                #distressed state: plane lights stop blinking
                self._unity_state.blinking_lights=False
                self._unity_state.turbolences=1.0
                self._unity_state.voices = {'volume' : 0.5, 'type' : 3}
                return self._unity_state
            case 5 if step < self.tot_steps / 35: #7
                self._unity_state.turbolences= 0.5
                self._unity_state.rain = 500
                return  self._unity_state
            case 6: #9
                self._unity_state.applauses = True
                self._unity_state.turbolences = 0
                self._unity_state.exposure += self._unity_state.exposure * 0.5
                return self._unity_state
            case _ :
                return self._unity_state
            