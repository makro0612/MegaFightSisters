import pygame as pg
from pygame.locals import (K_w,K_a,K_s,K_d,K_UP,K_LEFT,K_RIGHT,K_DOWN)
from characters.characterconfig import CHARACTERS
from config import WINDOWHEIGHT, WINDOWWIDTH

class Character:
    def __init__(self, character: str, playernumber: int, startpos: int):
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
        self.respawncounter = 0

        # key groups for input checks (index 0 = player1, 1 = player2)
        yourkeys = {
            "jump": (K_w, K_UP),
            "left": (K_a, K_LEFT),
            "down": (K_s, K_DOWN),
            "right": (K_d, K_RIGHT),
        }
        # get key for this player
        self.jump_key = yourkeys["jump"][playernumber]
        self.left_key = yourkeys["left"][playernumber]
        self.down_key = yourkeys["down"][playernumber]
        self.right_key = yourkeys["right"][playernumber]
        self.playernumber = playernumber

        # rect used for collisions (centered on the circle)
        self.rect = pg.Rect(int(self.x - self.size), int(self.y - self.size), self.size * 2, self.size * 2)

        self.font = pg.font.SysFont("segoeuiemoji", 50)

    def update(self, keys, objects: list[pg.Rect] | None = None):
        if self.alive:
        # horizontal movement
            if keys[self.left_key]:
                self.x -= self.speed
            if keys[self.right_key]:
                self.x += self.speed


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

            # ground collision
            if ((self.y + self.size) >= (WINDOWHEIGHT) 
                or (self.x + self.size) >= (WINDOWWIDTH)
                or (self.x - self.size) <= 0):
                self.health -= 1
                self.alive = False

            # object collision (landing): check collisions after movement and only if not dropping through
            if objects and not drop_through:
                temp_rect = pg.Rect(int(self.x - self.size), int(self.y), self.size*2, self.size*2)
                collided_index = temp_rect.collidelist(objects)
                if collided_index != -1 and self.vy >= 0:
                    platform = objects[collided_index]
                    # if we passed through the top of the platform this frame, snap to its top
                    if self.y - platform.top < -6:
                        self.y = platform.top - self.size * 2
                        self.vy = 0

        elif not self.alive:
            self.vy, self.vx = (0,0)
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
        pg.draw.rect(window,(0,255,0),self.rect)
        font_surface = self.font.render(str(f"{self.health}❤️"),True,(0,0,0))
        window.blit(font_surface,(WINDOWWIDTH*self.playernumber-font_surface.get_width()*(self.playernumber-0.1)*1.11,50))
    
