import pygame as pg
from maphelper import Object
from Maps import objects
from config import colors, WINDOWHEIGHT, WINDOWWIDTH

FPS = 60

pg.init()
window = pg.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
clock = pg.time.Clock()

map = [Object(*object) for object in objects]




def main():
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False

        window.fill(colors["BLUE"])
        for objects in map:
            Object.draw(objects,vindu=window)
        pg.display.flip()
        clock.tick(FPS)

    pg.quit()

if __name__ == "__main__":
    main()