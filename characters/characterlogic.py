import pygame as pg
from pygame.locals import (K_w,K_a,K_s,K_d,K_f,K_UP,K_LEFT,K_RIGHT,K_DOWN,K_RSHIFT)
from characters.characterconfig import CHARACTERS
from config import WINDOWHEIGHT, WINDOWWIDTH, COLORS
from pathlib import Path

class Character:



    IMAGE_DIR = Path(__file__).parent / "Sprites" / "PNG" / "Swordsman_lvl1" / "Without_shadow"
    FRAME_WIDTH = 64

    def getImageSpriteList(self, image_name: str, row:int) -> list[pg.Surface]:
        full_image = pg.image.load(self.IMAGE_DIR / image_name)
        # Finn antall frames basert på bildebredde
        num_frames = full_image.get_width() // self.FRAME_WIDTH
        
        # Dele opp bildet i frames, som lagres i en liste:
        frames = []
        for i in range(num_frames):
            # OBS: ANTAR at bildene er kvadratiske - bruker frame widht både som høye og bredde
            frame = full_image.subsurface(pg.Rect(i * self.FRAME_WIDTH, row*self.FRAME_WIDTH - self.FRAME_WIDTH, self.FRAME_WIDTH, self.FRAME_WIDTH))
            frames.append(frame)
        return frames
    
    def getSingleSpriteImage(self, image_name) -> pg.Surface:
        full_image = pg.image.load(self.IMAGE_DIR / image_name)
        return full_image



    def __init__(self, character: str, playernumber: int, startpos: tuple[int,int]):

        self.frames_run_left = self.getImageSpriteList("Swordsman_lvl1_Run_without_shadow.png",2)
        self.current_frame = 0
        # physics tuning
        self.RESPAWNTICKS = 60
        self.JUMPSPEED = 12    # initial jump velocity (px/frame)
        self.GRAVITY = 0.8     # gravity (px/frame^2)
        self.vy = 0            # vertical velocity

        self.attributes = CHARACTERS[character]
        self.speed = self.attributes["speed"]
        self.size = self.attributes["size"]  # pixel radius
        self.range = self.attributes["range"]
        self.strength = self.attributes["strength"]
        self.health = self.attributes["health"]
        self.jump_height = self.attributes["jump_height"]

        self.startpos = startpos
        self.x,self.y = startpos
        self.alive = True
        self.direction = None
        self.lastdirection = None
        self.respawncounter = 0
        self.attacked = False
        self.ATTACKEDTIMER = 10
        self.attackedcounter = 0
        self.attackeddirection = None
        self.ATTACKTIMER = 12
        self.attackcounter = 0

        # key groups for input checks (index 0 = player1, 1 = player2)
        yourkeys = {
            "jump": (K_w, K_UP),
            "left": (K_a, K_LEFT),
            "down": (K_s, K_DOWN),
            "right": (K_d, K_RIGHT),
            "attack": (K_f, K_RSHIFT)
        }
        # get key for this player
        self.jump_key = yourkeys["jump"][playernumber]
        self.left_key = yourkeys["left"][playernumber]
        self.down_key = yourkeys["down"][playernumber]
        self.right_key = yourkeys["right"][playernumber]
        self.attack_key = yourkeys["attack"][playernumber]
        self.playernumber = playernumber

        # rect used for collisions (centered on the circle)
        self.rect = pg.Rect(int(self.x - self.size), int(self.y - self.size), self.size * 2, self.size * 2)
        self.image_rect = pg.Rect(0,0,64,64)
        self.font = pg.font.SysFont("segoeuiemoji", 50)

    def update(self, keys, other_player, objects: list[pg.Rect] | None = None, map = None):
        if self.alive:
            if not self.attacked:
                # horizontal movement
                if keys[self.left_key]:
                    self.x -= self.speed
                    self.direction = "left"
                    self.lastdirection = -1

                if keys[self.right_key]:
                    self.x += self.speed
                    self.direction = "right"
                    self.lastdirection = 1

                if keys[self.left_key] == keys[self.right_key]:
                    self.direction = None
                
                # standing check (before moving) — used to allow jumping
                standing_index = -1
                if objects:
                    checkrect = self.rect
                    checkrect.y += 1
                    standing_index = checkrect.collidelist(objects)
                standing_on_object = standing_index != -1
                # jump: set upward velocity when on ground or standing on an object
                if keys[self.jump_key] and standing_on_object and self.vy >= 0:
                    self.vy = -self.JUMPSPEED

                # apply gravity and vertical motion
                self.vy += self.GRAVITY
                self.y += self.vy

                # allow dropping through platforms if down is held while falling
                drop_through = keys[self.down_key] and self.vy >= 0

                # edge collision
                if ((self.y + self.size) >= (WINDOWHEIGHT) 
                    or (self.x + self.size) >= (WINDOWWIDTH)
                    or (self.x - self.size) <= 0):
                    self.health -= 1
                    self.alive = False

                # object collision (landing): check collisions after movement and only if not dropping through
                if objects:
                    temp_rect = pg.Rect(int(self.x - self.size), int(self.y), self.size*2, self.size*2)
                    collided_index = temp_rect.collidelist(objects)
                    if collided_index != -1 and self.vy >= 0:
                        platform = objects[collided_index]
                        if  not drop_through or not map[collided_index].platform:
                            # if we passed through the top of the platform this frame, snap to its top
                            if self.y - platform.top < 0:
                                self.y = platform.top - self.size * 2
                                self.vy = 0

                if keys[self.attack_key] and self.attackcounter == 0:
                    if ((self.x + self.size * self.lastdirection - other_player.x- other_player.size * self.lastdirection - self.range * self.lastdirection)*self.lastdirection < 0 and
                    abs(self.x + self.size - other_player.x- other_player.size) - self.range < 0
                    and abs(self.y + self.size - other_player.y- other_player.size) < self.range):
                        other_player.attacked = True
                        other_player.attackeddirection = self.lastdirection
                    self.attackcounter = self.ATTACKTIMER
                else:
                    self.attackcounter = max(self.attackcounter-1,0)

            elif self.attacked:
                self.vy
                self.x += 10*self.attackeddirection
                self.y -= 1
                
                self.attackedcounter += 1
                if self.attackedcounter == self.ATTACKEDTIMER:
                    self.attacked = False
                    self.attackedcounter = 0

        elif not self.alive:
            self.vy = 0
            self.x,self.y = (-100,-100)
            if self.health > 0:
                self.respawncounter += 1
                if self.respawncounter == self.RESPAWNTICKS:
                    self.x,self.y = self.startpos
                    self.respawncounter = 0
                    self.alive = True
        
        # update rect position (centered)
        self.rect.topleft = (int(self.x - self.size), int(self.y))


    def draw(self, window: pg.Surface):
        current_frame_image = self.frames_run_left[self.current_frame]
        #pg.draw.rect(window,COLORS["RED"],self.rect)
        self.image_rect.center = self.rect.center
        window.blit(current_frame_image, self.image_rect)



        font_surface = self.font.render(str(f"{self.health}❤️"),True,COLORS["BLACK"])
        #0.1 og -0.11 er justification av skriften
        window.blit(font_surface,(WINDOWWIDTH*self.playernumber-font_surface.get_width()*(self.playernumber-0.1)*1.11 ,50))
    
