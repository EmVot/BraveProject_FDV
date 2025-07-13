from abc import ABC, abstractmethod
import math

from BraveProject_FDV.multimotionDummy import EmotionalState
from BraveProject_FDV.Agent import UnityMessage

class Session(ABC):
    _sessions = {}
    
    def __new__(cls, session_id, tau=0):

        if session_id in cls._sessions:
            instance = cls._sessions[session_id]()
            instance.tau = tau
            return instance
        raise ValueError(f"Session {session_id} not found")
    
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
        super().__init__(session_id)
        self.tot_steps = tot_steps
        self.tau = tau
        self.points = [
            (0.8003965398535,-0.6310763224595),
            (0.413991411612474, 139.89909245378777),
            (0.3416666666666667, -102.68038349181982),
            (0.9014586944379525, 94.7724388316847),
            (0.9204467514322717, 121.67546873810922),
            (0.8993114650170492, 141.6221079228427),
            (0.9014586944379525, 94.7724388316847),
            (0.8274794391537607, 161.20011484134733),
            (0.3416666666666667, -102.68038349181982)
        ]

    def map_state(self, state, step) -> UnityMessage:
        closest_index = next(
                (i for i, point in enumerate(self.points) if self.is_within_radius((state.valence, state.arousal), point)),
                -1
            )

        match closest_index:
            case 0:  # Primo punto nel raggio
                pass
            case 1:  # Secondo punto nel raggio
                pass
            case 2:  # Terzo punto nel raggio
                pass
            case _:  # Nessun punto nel raggio
                pass

        return f"Session1: {state} -> message_v1"