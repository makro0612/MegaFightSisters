import pygame as pg
import os

class Box():

    def __init__(self, x:int,y:int,length:int,height:int, color, liste:list) -> None:
        self.rect = pg.Rect(x,y,length,height)
        self.color = color
        liste.append(self)
    
    def __repr__(self) -> str:
        return f"Obstacle som er på {self.rect.x}, x, og {self.rect.y}, y "
        

    def draw(self,vindu):
        pg.draw.rect(surface=vindu, color=self.color, rect=self.rect)