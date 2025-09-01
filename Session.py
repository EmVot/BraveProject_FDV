import math
from abc import ABC, abstractmethod

from UnityState import UnityState
from multimotionDummy import EmotionalState


class Session(ABC):
    _sessions = {}
    
    def __new__(cls, session_id, tau=0.01):
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
    def map_state(self, state: EmotionalState, step: int):
        pass
    
    def define_references(self, dict_ref):
        self.dict_ref = dict_ref

    def is_within_radius(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        print(distance)
        
        return distance <= self.tau

class Session1(Session):
    def __init__(self, session_id, tau=0.05,tot_steps=55):
        super().__init__(session_id, tau)
        self.last_index = None
        self.tot_steps = tot_steps
        self.tau = tau
        self._unity_state = UnityState()
        self.ref_points = [
            (0.7232124698884, -0.6849506327398), # calm - 0
            (-0.2795869814271,0.2579723123494), # suspicious - 1
            (-0.0473321454708,-0.2937238784429), # worried - 2
            (-0.06,0.92), #alarmed - 3
            (-0.3809788479506,0.8204066501303), # afraid - 4
            (-0.7063574248073,0.6208324950319),# distressed - 5
            (-0.8425703922493,0.2236834667662),#bitter- 6  
        ]
        with open('therapist_transcripts.txt', 'r') as file:
            self.therapist_transcripts = file.readlines()
            
    def get_therapist_transcript(self, step):
        return self.therapist_transcripts[step]
    
    def map_state(self, state, step):
        # closest_index = next(
        #         (i for i, point in enumerate(self.ref_points) if self.is_within_radius(state, point)),
        #         -1
        #     )
        #print(f"Closest index: {closest_index}")
        print("State: ", state)
        match step:
            case 5: #2
                self._unity_state.exposure = self._unity_state.exposure + 0.5       #9.5
                message = {"exposure": self._unity_state.exposure}
                return message, self._unity_state
            case 10: #3
                print("case 1 (2)")
                self._unity_state.exposure = self._unity_state.exposure +1      #10.5
                self._unity_state.rain = 1000
                message = {"exposure": self._unity_state.exposure, "rain": self._unity_state.rain}
                return message, self._unity_state
            case 15: #4
                print("case 2 (3)")
                self._unity_state.exposure = self._unity_state.exposure + 1.5      #12
                self._unity_state.rain = 10000
                self._unity_state.voices = "worried"
                self._unity_state.turbolence = 0.003
                message = {
                    "exposure": self._unity_state.exposure,
                    "rain": self._unity_state.rain,
                    "voices": self._unity_state.voices,
                    "turbolence": self._unity_state.turbolence}
                return message, self._unity_state
            case 20: #5
                print("case 3 (4)")
                self._unity_state.lightning = True
                self._unity_state.rain = 20000
                self._unity_state.rumbling = True
                self._unity_state.turbolence = 0.010
                message = {
                    "rain": self._unity_state.rain,
                    "lightning": self._unity_state.lightning,
                    "rumbling": self._unity_state.rumbling,
                    "turbolence": self._unity_state.turbolence
                }
                return message, self._unity_state
            #case 21:
                #self._unity_state.lightning = False
                #return {}, self._unity_state
            case 25:
                self._unity_state.turbolence = 0.015
                self._unity_state.voices = "panic"
                self._unity_state.oxygenMasks = True
                message = {
                    "turbolence": self._unity_state.turbolence,
                    "voices": self._unity_state.voices,
                    "oxygenMasks": self._unity_state.oxygenMasks,
                }
                return message, self._unity_state
            
            case 30: #6
                self._unity_state.turbolence = 0.010
                message = {
                    "turbolence": self._unity_state.turbolence,
                }
                return message, self._unity_state
            case 35: #7
                print("case 5 (6)")
                #distressed state: plane lights stop blinking
                self._unity_state.turbolence = 0.005
                self._unity_state.voices = "worried"
                self._unity_state.exposure = self._unity_state.exposure - 0.5
                self._unity_state.rain = 15000
                message = {
                    "turbolence": self._unity_state.turbolence,
                    "voices": self._unity_state.voices,
                    "exposure": self._unity_state.exposure,
                    "rain": self._unity_state.rain
                }
                return message, self._unity_state
            
            case 40: #8
                print("case 5 (7)")
                self._unity_state.turbolence = 0.0
                self._unity_state.rain = 5000
                self._unity_state.exposure = self._unity_state.exposure - 1
                self._unity_state.oxygenMasks = False
                message  = {
                    "oxygenMasks": self._unity_state.oxygenMasks,
                    "turbolence": self._unity_state.turbolence,
                    "rain": self._unity_state.rain,
                    "exposure": self._unity_state.exposure,
                }
                return  message, self._unity_state
            case 45: #9
                self._unity_state.exposure -= 1.5
                self._unity_state.rain = 0
                self._unity_state.voices = "calm"
                self._unity_state.rumbling = False
                message = {
                    "voices": self._unity_state.voices,
                    "rumbling": self._unity_state.rumbling,
                    "rain": self._unity_state.rain,
                    "exposure": self._unity_state.exposure,
                }
                return message, self._unity_state
                
            case _ :
                print("here")
                return {}, self._unity_state
            