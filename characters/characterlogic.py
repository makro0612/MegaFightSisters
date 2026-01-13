import pygame as pg
from pygame.locals import (K_w,K_a,K_s,K_d,K_UP,K_LEFT,K_RIGHT,K_DOWN)
from characters.characterconfig import characters

class Character:
    def __init__(self,character:str, playernumber):
        self.JUMPSPEED = 10
        self.GRAVITY = 10
        self.attributes = characters[character]
        self.speed = self.attributes["speed"]
        self.size = self.attributes["size"]
        self.range = self.attributes["range"]
        self.strength = self.attributes["strength"]
        self.health = self.attributes["health"]
        self.jump_height = self.attributes["jump_height"]

        self.x = 0
        self.y = 0

        self.playernumber = playernumber

    def update(self, keys):
        # key groups for input checks
        yourkeys = {
            "jump": (K_w, K_UP),
            "left": (K_a, K_LEFT),
            "down": (K_s, K_DOWN),
            "right": (K_d, K_RIGHT),
        }
        if any(keys[k] for k in yourkeys["jump"]):
            self.y -= self.JUMPSPEED
        if any(keys[k] for k in yourkeys["down"]):
            self.y += self.GRAVITY
        if any(keys[k] for k in yourkeys["left"]):
            self.x -= self.speed
        if any(keys[k] for k in yourkeys["right"]):
            self.x += self.speed

    def draw(self, window):
        pg.draw.circle(window, (255,0,0), (int(self.x), int(self.y)), self.size) 
