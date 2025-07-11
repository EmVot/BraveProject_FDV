from dataclasses import dataclass
from typing import List, Callable, Optional


@dataclass
class State:
    arousal: float = 0.0
    valence: float = 0.0
    time: int = 0
    rain: float = 0.0
    lightings: bool = False
    exposure: float = 0.0
    oxMasks: bool = False
    turbolences: float = 0.0
    voices: dict[float,int]
    rumbling: bool = 0.0

@dataclass
class Transition:
    condition: Callable[[State], bool]
    next_state: State

class StateMachine:
    def __init__(self, initial_state: State):
        self.current_state = initial_state
        self.transitions: List[Transition] = []

    def add_transition(self, transition: Transition):
        self.transitions.append(transition)

    def step(self):
        for transition in self.transitions:
            if transition.condition(self.current_state):
                print(f"Transitioning from {self.current_state} to {transition.next_state}")
                self.current_state = transition.next_state
                return
        print("No valid transition found.")

    def get_state(self) -> State:
        return self.current_state

# Condizione per transizione
def condition_to_next_example(state: State) -> bool:
    return (
        state.time == "morning"
        and not state.rain
        and not state.lightings
        and not state.exposure
)

# === ESEMPIO DI UTILIZZO ===

# Stato iniziale
#initial = State(arousal=0.3, valence=0.1, time="morning", rain=False, lightings=False, exposure=False)
#fsm = StateMachine(initial)

# Stato successivo possibile
#next_state = State(arousal=0.6, valence=0.5, time="afternoon", rain=False, lightings=True, exposure=True)

#fsm.add_transition(Transition(condition=condition_to_next, next_state=next_state))

# Esegui una transizione
#fsm.step()

# Stato corrente
#print("Stato attuale:", fsm.get_state())