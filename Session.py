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
        r1, theta1 = point1
        r2, theta2 = point2
        
        x1, y1 = r1 * math.cos(theta1), r1 * math.sin(theta1)
        x2, y2 = r2 * math.cos(theta2), r2 * math.sin(theta2)
        
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        return distance <= self.tau

class Session1(Session):
    def map_state(self, state, step) -> UnityMessage:


        return f"Session1: {state} -> message_v1"
