import numpy as np

SCALE = 6
SER = 0.001      #Standard Emotional Radius -> radius for the proobability circle associated to each emotion

probable_emotions = {
        'impressed':(2.35,-0.41),
        'worried':(-0.45,-2.0),
        'hesitant':(-1.89,-4.35),
        'ashamed':(-2.65,-3),
        'embarrased':(-1.9,-3.59),
        'anxious':(-4.35,-4.8),
        'desperate':(-4.8,-3),
        'depressed':(-4.85,-2.8),
        'bitter':(-4.7,1.6),
        'discontented':(-4,2),
        'distressed':(-4.23,3.35),
        'frustrated':(-3.6,2.38),
        'souspicoius':(-1.9,1.6),
        'annoyed':(-2.65,3.98),
        'impatient':(-0.3,1.8),
        'afraid':(-2.4,4.7),
        'angry':(-0.68,4.7),
        'alarmed':(-0.45,5.39),
        'tense':(-0.1,5.15),
    }


Norm_emotions = {
    'impressed': (0.39167, -0.06833),
    'worried': (-0.075, -1/3),
    'hesitant': (-0.315, -0.725),
    'ashamed': (-0.44167, -0.5),
    'embarrased': (-0.31667, -0.59833),
    'anxious': (-0.725, -0.8),
    'desperate': (-0.8, -0.5),
    'depressed': (-0.80833, -0.46667),
    'bitter': (-0.78333, 0.266667),
    'discontented': (-2/3, 1/3),
    'distressed': (-0.705, 0.55833),
    'frustrated': (-3/5, 0.39667),
    'souspicoius': (-0.31667, 0.26667),
    'annoyed': (-0.4412, 0.66333),
    'impatient': (-0.05, 0.3),
    'afraid': (-0.4, 0.78333),
    'angry': (-0.11333, 0.78333),
    'alarmed': (-0.075, 0.89833),
    'tense': (-0.01667, 0.85833)
    }

neighborhood = {
        'ashamed-embarassed': {
            'guitly':(-2.4,-2.6),
            'languid':(-1.35,-2.9),
            'hesitant':(-1.89,-4.35),
            },
        'desperate-depressed':{
            'gloomy':(-5.2,-2.75)
            },

        'discontented-bitter':{
            'insulted':(-4.49,1.2),
            'frustrated':(-3.55,2.35),
        },
        'distressed-frustrated-suspicious':{
            'discontented':(-4,2),
            'disgusted':(-4,2.95),
        },
        'afraid':{
            'envious':(-1.59,4.9)
        },
        'annoyed-impatient':{
            'indignant':(-1.42,2.8),
            'jealous':(-0.45,3.4)
        }
        
    }

neighborhood_norm = {
        'ashamed-embarassed':{
            'guitly':(-0.39999999999999997, -0.43333333333333335),
            'languid':(-0.225, -0.48333333333333334),
            'hesitant':(-0.315, -0.725),
            },

        'desperate-depressed':{
            'gloomy':(-0.4583333333333333, -0.08666666666666667)
            },

        'discontented-bitter':{
            'frustrated':(-0.5916666666666667, 0.39166666666666666),
            'insulted':(-0.7483333333333334, 0.19999999999999998),
        },

        'distressed-frustrated-suspicious':{
            'discontented':(-2/3,1/3),
            'disgusted':(-2/3,0.49166667)
        },
        'afraid':{
            'envious':(-0.265, 0.8166666666666668)
        },
        'annoyed-impatient':{
            'indignant':(-0.237, 0.467),
            'jealous':(-0.075,0.567)
        }

    }


probability_regions = {
    
    'positive-active': '{x^2+y^2+1<=0 and x>0 and y>0}',
    'positive-inactive': '{x^2+y^2+1<=0 and x>0 and y<0}',
    'negative-inactive': '{x^2+y^2+1<=0 and x<0 and y<0}',
    'negative-active': '{x^2+y^2+1<=0 and x<0 and y>0}',
    'impressed':'(x-0.391666666)^(2)+(y+0.068333)^(2)≤.001',
    'worried':'(x+0.075)^(2)+(y+0.333333)^(2)≤.001',
    'ashamed-imbarassed':'0.8737859996627*x^(2) + 0.7866666666667*x*y + 1.0643637774405*y^(2) + 1.0946321608554*x + 1.4673039933333*y <= -0.6043640864553',
    'depressed-desperate':'(x + 0.8041666666667)^(2) + (y + 0.4833333333333)^(2) <= 0.0009662262114',
    'discontented-bitter':'1.0991281904577*x^(2) - 0.9955555555556*x*y + 1.6857948571243*y^(2) + 1.8924025428303*x - 1.7332546920524*y <= -0.9397141180262',
    'afraid':'(x+0.48333333333333334)^2 + (y-0.7833333333333333)^2 <= 0.01',
    'angry':'(x+0.11333333333333334)^2 + (y-0.8983333333333333)^2 <=0.001',
    'alarmed-tense':'0.9291093605484*x^(2) + 0.5973333333333*x*y + 1.1598649161039*y^(2) - 0.4394894197275*x - 2.0101182581781*y <= -0.870774756474',
    'hesitant':'(x+0.315)^2+(y+0.725)^2<=0.001'

    }


polar_emotions ={
    'impressed': (0.39758297526707836, -9.896671967669098),
    'worried': (0.3416666666666667, -102.68038349181982),
    'hesitant': (0.7904745410195069, -113.48411529050487),
    'ashamed': (0.6671352519875144, -131.45523354440513),
    'embarrased': (0.676964220292, -117.88993764054699),
    'anxious': (1.079641144084459, -132.1844433157888),
    'desperate': (0.9433981132056604, -147.9946167919165),
    'depressed': (0.9333705349728775, -150.0013184604715),
    'bitter': (0.8274794391537607, 161.20011484134733),
    'discontented': (0.7453559924999299, 153.434948822922),
    'distressed': (0.8993114650170492, 141.6221079228427),
    'frustrated': (0.7192666017857665, 146.53086626144034),
    'souspicoius': (0.413991411612474, 139.89909245378777),
    'annoyed': (0.8062757317168585, 124.64271918104106),
    'impatient': (0.30413812651491096, 99.46232220802563),
    'afraid': (0.9204467514322717, 121.67546873810922),
    'angry': (0.7914894538498637, 98.23247707459585),
    'alarmed': (0.9014586944379525, 94.7724388316847),
    'tense': (0.8584951303815818, 91.1123996162978)
}

epsilon = 1e-8

polar_regions = {
    '1':{
        'radius':{
            'min':0.85,
            'max':1
        },
        'angle':{
            'min':90,
            'max':95.45
        }
    },
    '2':{
        'radius':{
            'min':0,
            'max':0.85-epsilon
        },
        'angle':{
            'min':90,
            'max':95.45
        }
    },
    '3':{
        'radius':{
            'min':0,
            'max':np.sqrt(.7)
        },
        'angle':{
            'min':95.45,
            'max':110.05
        }
    },
    '4':{
        'radius':{
            'min':np.sqrt(.7)+epsilon,
            'max':1
        },
        'angle':{
            'min':95.45,
            'max':110.05
        }
    },
    '5':{
        'radius':{
            'min':0,
            'max':0.7-epsilon
        },
        'angle':{
            'min':110.05,
            'max':125.53
        }
    },
    '6':{
        'radius':{
            'min':0.7,
            'max':np.sqrt(0.7)-epsilon
        },
        'angle':{
            'min':110.05,
            'max':125.53
        }
    },
    '7':{
        'radius':{
            'min':np.sqrt(0.7),
            'max':1
        },
        'angle':{
            'min':110.05,
            'max':125.53
        }
    },
    '8':{
        'radius':{
            'min':0,
            'max':1
        },
        'angle':{
            'min':125.53,
            'max':135
        }
    },
    '9':{
        'radius':{
            'min':0,
            'max':0.16
        },
        'angle':{
            'min':135,
            'max':149.88
        }
    },
    '10':{
        'radius':{
            'min':0.16,
            'max':0.8
        },
        'angle':{
            'min':135,
            'max':149.88
        }
    },
    '11':{
        'radius':{
            'min':0.8+epsilon,
            'max':np.sqrt(0.75)-epsilon
        },
        'angle':{
            'min':135,
            'max':149.88
        }
    },
    '12':{
        'radius':{
            'min':np.sqrt(0.75),
            'max':1
        },
        'angle':{
            'min':135,
            'max':149.88
        }
    },
    '13':{
        'radius':{
            'min':0,
            'max':0.7-epsilon
        },
        'angle':{
            'min':149.88,
            'max':163.3
        }
    },
    '14':{
        'radius':{
            'min':0.7,
            'max':np.sqrt(0.75)
        },
        'angle':{
            'min':149.88,
            'max':163.3
        }
    },
    '15':{
        'radius':{
            'min':np.sqrt(0.75)+epsilon,
            'max':1
        },
        'angle':{
            'min':149.88,
            'max':163.3
        }
    },
    '16':{
        'radius':{
            'min':0,
            'max':1
        },
        'angle':{
            'min':163.3,
            'max':180
        }
    },
    '17':{
        'radius':{
            'min':0,
            'max':1
        },
        'angle':{
            'min':180,
            'max':206.56
        }
    },
    '18':{
        'radius':{
            'min':0,
            'max':0.89
        },
        'angle':{
            'min':206.56,
            'max':213.82
        }
        },
    '19':{
        'radius':{
            'min':0.89,
            'max':1
        },
        'angle':{
            'min':206.56,
            'max':213.82

        }
    },
    '20':{
        'radius':{
            'min':0,
            'max':1
        },
        'angle':{
            'min':213.82,
            'max':225
        }
    },
    '21':{
        'radius':{
            'min':0,
            'max':0.6-epsilon
        },
        'angle':{
            'min':225,
            'max':244.43
        }
    },
    '22':{
        'radius':{
            'min':0.6,
            'max':0.74
        },
        'angle':{
            'min':225,
            'max':244.43
        }
    },
    '23':{
        'radius':{
            'min':0.74+epsilon,
            'max':1
        },
        'angle':{
            'min':225,
            'max':244.43
        }
    },
    '24':{
        'radius':{
            'min':1+epsilon,
            'max':np.sqrt(1.28)
        },
        'angle':{
            'min':225,
            'max':230.6
        }
    },
    '25':{
        'radius':{
            'min':0,
            'max':0.6-epsilon
        },
        'angle':{
            'min':244.43,
            'max':256.34
        }
    },
    '26':{
        'radius':{
            'min':0.6,
            'max':0.83
        },
        'angle':{
            'min':244.43,
            'max':256.34
        }
    },
    '27':{
        'radius':{
            'min':0.83+epsilon,
            'max':1
        },
        'angle':{
            'min':244.43,
            'max':256.34
        }
    },
    '29':{
        'radius':{
            'min':0,
            'max':0.3
        },
        'angle':{
            'min':256.34,
            'max':270
        }
    },
    '30':{
        'radius':{
            'min':0.3,
            'max':0.4
        },
        'angle':{
            'min':256.34,
            'max':270
        }
    },
    '31':{
        'radius':{
            'min':0.4+epsilon,
            'max':1
        },
        'angle':{
            'min':256.34,
            'max':270
        }
    },
    '32':{
        'radius':{
            'min':0,
            'max':1
        },
        'angle':{
            'min':270,
            'max':309.4
        }
    },
    '33':{
        'radius':{
                'min':0,
                'max':np.sqrt(0.87)
        },
        'angle':{
                'min':309.44,
                'max':320.31
        }
    },
    '34':{
        'radius':{
                'min':np.sqrt(0.87),
                'max':1
        },
        'angle':{
                'min':309.44,
                'max':320.31
        }
    },
    '35':{
        'radius':{
                'min':0,
                'max':1
        },
        'angle':{
                'min':320.31,
                'max':344.43
        }
    },
    '36':{
        'radius':{
                    'min':0,
                    'max':0.35-epsilon
            },
            'angle':{
                    'min':344.43,
                    'max':360
            }
    },
    '37':{
        'radius':{
                    'min':0.35,
                    'max':0.45
            },
            'angle':{
                    'min':344.43,
                    'max':360
            }
    },
    '38':{
        'radius':{
                    'min':0.45,
                    'max':1
            },
            'angle':{
                    'min':344.43,
                    'max':360
            }
    },
    '39':{
        'radius':{
                    'min':0,
                    'max':1
            },
            'angle':{
                    'min':0,
                    'max':90
            }
    }
}

def normalize(coordinates: tuple)->tuple:
    '''Normalizes the coordinates onto the unitary cinmurference'''
    return (coordinates[0]/SCALE,coordinates[1]/SCALE)

def cartesian_to_polar(coordinates:tuple)->tuple:
    '''
    Converts cartesian coordinates to polar coordinates
    '''
    
    return (np.sqrt(coordinates[0]**2+coordinates[1]**2),np.degrees(np.arctan2(coordinates[1],coordinates[0])))

if __name__ == '__main__':
        print(normalize((-1.42,2.8)))
        print(normalize((-0.45,3.4)))