# Sprite classes for platform game
import pygame as pg
from settings import *
from random import choice
vec = pg.math.Vector2

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height,scaler=0.5):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (int(width*scaler), int(height*scaler)))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.state = 'idle'
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (60, HEIGHT - 115)
        self.collideRect =  pg.rect.Rect((0, 0), (int(self.rect.width*2/3), int(self.rect.height*2/3) ))
        self.collideRect.center = self.rect.center

        self.pos = vec(100, HEIGHT - 115)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.standing_frames = [self.game.spritesheet2.get_image(0, 0, 215, 210),
                                self.game.spritesheet2.get_image(340, 0, 215, 210)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet2.get_image(340, 472, 215, 210),
                              self.game.spritesheet2.get_image(0, 472, 215, 210)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frames = [self.game.spritesheet2.get_image(0, 236, 215, 210),
                            self.game.spritesheet2.get_image(340, 236, 215, 210)]
        for frame in self.jump_frames:
            frame.set_colorkey(BLACK)


    def jump(self):
        # jump only if standing on a platform
        if self.pos.y == HEIGHT - 115:
            self.vel.y = -PLAYER_JUMP
            self.game.jump_sound.play()

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()

        self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        
        # Updates y position of player
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.midbottom = self.pos
        self.collideRect.center = self.rect.center

        # Move background
        delta = self.vel.x + 0.5 * self.acc.x
        self.game.background.rect.x -= delta
        self.game.background2.rect.x = self.game.background.rect.right
        
        # Move obstacles
        for obs in self.game.obstacles:
            obs.rect.x -= delta
        #print(self.vel.x)

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            if self.pos.y < HEIGHT - 115:
                self.state = 'jumping'
            else:
                self.state = 'walking'
        else:
            self.state = 'idle'
        # show walk animation
        if self.state == 'walking':
            if now - self.last_update > 180:
                animate_walking(self,now)
                
        elif self.state == 'jumping':
            if now - self.last_update > 180:
                animate_jumping(self,now)
                
        # show idle animation
        else: #self.state == 'idle':
            if now - self.last_update > 350:
                animate_idle(self,now)
                

######################################################
#DECORADOR DE ANIMACION (caminar, saltar, idle):

def decorador_animate(f):
    def meta(self,now,**kwargs):
        print("entra al decorador")
        self.last_update = now
        self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
        bottom = self.rect.bottom

        f(self,now)

        self.rect = self.image.get_rect()
        self.rect.bottom = bottom

        print("se ejecuto %s" % f.__name__)
    return meta

@decorador_animate
def animate_walking(self,now):
    if self.vel.x > 0:
        self.image = self.walk_frames_r[self.current_frame]
    else:
        self.image = self.walk_frames_l[self.current_frame]

@decorador_animate
def animate_jumping(self,now):
    self.image = self.jump_frames[self.current_frame]

@decorador_animate
def animate_idle(self,now):
    self.image = self.standing_frames[self.current_frame]

######################################################




class Background(pg.sprite.Sprite):
    def __init__(self, game,x=0):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        sc = 6/9
        self.image = self.game.spritesheet3.get_image(0, 174, 1920, 1080,sc)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x,y=HEIGHT-200):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        sc = 0.3
        images = [self.game.spritesheet1.get_image(0, 0, 172, 277,sc)]
                  #self.game.spritesheet.get_image(0, 95, 315, 90,sc)]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
