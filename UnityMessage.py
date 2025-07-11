from dataclasses import dataclass, field

lightining_json = {
    'lightinigs':bool
}

exposure_json = {
    'min':float,
    'max':float,
    'exposure':float
}

rain_json = {
    'min' : 0.0,
    'max' : 2e4,
    'rain':float
}

flashes_json = {
    'flashes':bool
}

turbolences_json = {
    'min':0.0,
    'max':2.0,
    'pace': .1,
    'turbolescences':float
}

voices_json = {
    'voice':{
        'voice1':1,
        'voice2':2,
        'voice3':3,
    },
    'volume':{
        'intensity':float,
        'min':0.0,
        'max':1.0,
        'step':.1
    }
}

oxmasks_json = {
    'masks': bool
}

rumbling_json = {
    'rumbling':bool
}


END_SIGNAL = "end"

@dataclass
class UnityMessage:

    arousal: float = 0.0
    valence: float = 0.0
    time: int = 0
    rain: float = 0.0
    lightings: bool = False
    exposure: float = 0.0
    oxMasks: bool = False
    turbolences: float = 0.0
    voices: dict = field(default_factory=lambda: {"volume":0.0,'type':1})
    rumbling: bool = False

    def __init__(self, arousal: float = 0.0,
                    valence: float = 0.0,
                    time: int = 0,
                    rain: float = 0.0,
                    lightings: bool = False,
                    exposure: float = 0.0,
                    oxMasks: bool = False,
                    turbolences: float = 0.0,
                    voices = None,
                    rumbling: bool = True):
        self.arousal = arousal
        self.valence = valence
        self.time = time
        self.rain= rain
        self.lightings = lightings
        self.exposure = exposure
        self.oxMasks = oxMasks
        self.turbolences = turbolences
        self.voices = voices
        self.rumbling = rumbling
