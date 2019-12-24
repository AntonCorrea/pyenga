
#game settings

#WIDTH = 256*3
#HEIGHT = 150*s
WIDTH = 640
HEIGHT = 512
FPS = 120


FRICTION = 9999999
MASS = 0.1
GRAVITY = -0.1
#(0..1)
ELASTICITY = 0
MAX_VEL = 10
VEL_DAMP = 0.9

DIMENSIONS = [	(30,30),
				(60,30),
				(90,30),
				(120,30)]

MAP =   [
		[1,1,1],
		[2,2],
		[3],
		[4,4],
        ]

TILE = 32

COLORS ={	"BLACK" : (0,0,0),
			"WHITE" : (255,255,255),
			"RED" : (255,0,0),
			"BLUE" : (0,0,255),
			"LIME" : (0,255,0),
			"YELLOW" : (255,255,0),
			"CYAN" : (0,255,255),
			"MAGENTA" : (255,0,255),
			"SILVER" : (192,192,192),
			"GRAY" : (128,128,128),
			"MAROON" : (128,0,0),
			"OLIVE" : (128,128,0),
			"GREEN" : (0,128,0),
			"PURPLE" : (128,0,128),
			"TEAL" :  (0,128,128),
			"NAVY" : (0,0,128)
		}

COLOR_DEBUG = COLORS["CYAN"]