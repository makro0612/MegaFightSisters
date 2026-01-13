import pygame as pg
from pygame.locals import (K_w,K_a,K_s,K_d,K_UP,K_LEFT,K_RIGHT,K_DOWN)
from characters.characterconfig import characters
from config import WINDOWHEIGHT, WINDOWWIDTH

class Character:
    def __init__(self, character: str, playernumber: int):
        # physics tuning
        self.JUMPSPEED = 12    # initial jump velocity (px/frame)
        self.GRAVITY = 0.8     # gravity (px/frame^2)
        self.vy = 0            # vertical velocity

        self.attributes = characters[character]
        self.speed = self.attributes["speed"]
        self.size = self.attributes["size"]  # pixel radius
        self.range = self.attributes["range"]
        self.strength = self.attributes["strength"]
        self.health = self.attributes["health"]
        self.jump_height = self.attributes["jump_height"]

        self.playernumber = playernumber

        # starting position based on player number (x,y are center coords)
        margin = 50
        if self.playernumber == 0:
            self.x = margin + self.size
        else:
            self.x = WINDOWWIDTH - margin - self.size
        self.y = WINDOWHEIGHT - self.size - 10

        # rect used for collisions (centered on the circle)
        self.rect = pg.Rect(int(self.x - self.size), int(self.y - self.size), self.size * 2, self.size * 2)

    def update(self, keys, objects: list[pg.Rect] | None = None):
        # key groups for input checks (index 0 = player1, 1 = player2)
        yourkeys = {
            "jump": (K_w, K_UP),
            "left": (K_a, K_LEFT),
            "down": (K_s, K_DOWN),
            "right": (K_d, K_RIGHT),
        }
        # get key for this player
        jump_key = yourkeys["jump"][self.playernumber]
        left_key = yourkeys["left"][self.playernumber]
        down_key = yourkeys["down"][self.playernumber]
        right_key = yourkeys["right"][self.playernumber]

        # horizontal movement
        if keys[left_key]:
            self.x -= self.speed
        if keys[right_key]:
            self.x += self.speed

        # clamp x to window
        self.x = max(self.size, min(self.x, WINDOWWIDTH - self.size))

        # check standing on ground or object (use center-based y)
        on_ground = (self.y + self.size) >= (WINDOWHEIGHT - 10)
        touching_index = -1
        if objects:
            touching_index = self.rect.collidelist(objects)
        touching_object = touching_index != -1

        # jump: set upward velocity when on ground or standing on an object
        if keys[jump_key] and (on_ground or touching_object) and self.vy >= 0:
            self.vy = -self.JUMPSPEED

        # apply gravity and vertical motion
        self.vy += self.GRAVITY
        prev_y = self.y
        self.y += self.vy

        # ground collision
        if (self.y + self.size) >= (WINDOWHEIGHT - 10):
            self.y = WINDOWHEIGHT - 10 - self.size
            self.vy = 0

        # object collision (landing)
        if touching_object and self.vy >= 0:
            platform = objects[touching_index]
            # if we passed through the top of the platform this frame, snap to its top
            if (prev_y + self.size) <= platform.top <= (self.y + self.size):
                self.y = platform.top - self.size
                self.vy = 0

        # update rect position (centered)
        self.rect.topleft = (int(self.x - self.size), int(self.y - self.size))

    def draw(self, window):
        pg.draw.circle(window, (255, 0, 0), (int(self.x), int(self.y)), self.size*2) 
