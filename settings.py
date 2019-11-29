# Game options/settings
TITLE = "Jumpy!"
WIDTH = 1280
HEIGHT = 720
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
PLAYER = "dino2.png"
BACKGROUND = 'bg2.jpg'
OBSTACLES = 'cactus2.png'
OBSTACLES_POS = [int(x*WIDTH/4)+WIDTH//5 for x in range(4)]
OBSTACLES_POS2 = [int(x*WIDTH) for x in [0.21,0.42,0.63,0.86]]

# Define sounds
JUMP_SOUND = 'Jump.wav'
HIT_SOUND = 'Hit.wav'
INIT_MUSIC = 'Happy Tune.ogg'
GAMEOVER_MUSIC = 'Yippee.ogg'
MUSIC_FADE = 200

# Player properties
PLAYER_ACC = 0.55
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = BLACK #LIGHTBLUE
