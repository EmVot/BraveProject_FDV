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
class UnityState:
    exposure: float = 0.0 #r:9-12, s:0.1
    rain: float = 0.0 #r:0-2e4 s:100
    flash: bool = False
    turbolence: float = 0.0  # r:0-0.015 s:0.001
    rumbling: bool = False
    oxygenMasks: bool = False
    voices: str = "calm" # 'calm', 'worried', 'panic'
    

    def __init__(self,
                    exposure: float = 9.0,
                    rain: float = 0.0,
                    flash: bool = False,
                    turbolence: float = 0.0,
                    rumbling: bool = False,
                    oxygenMasks: bool = False,
                    voices = 'calm',
                    ):
        self.rain = rain
        self.flash = flash
        self.exposure = exposure
        self.oxygenMasks = oxygenMasks
        self.turbolence = turbolence
        self.voices = voices
        self.rumbling = rumbling