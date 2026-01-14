import pygame as pg
from maphelper import Object
from Maps import MAPS
from config import colors, WINDOWHEIGHT, WINDOWWIDTH, FPS
from characters.characterlogic import Character

pg.init()
window = pg.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
clock = pg.time.Clock()

map = [Object(*object) for object in MAPS["basic"]["objects"]]

player1 = Character("basic", 0,MAPS["basic"]["startpos"][0])
player2 = Character("basic", 1,MAPS["basic"]["startpos"][1])

def main():
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False

        window.fill(colors["WHITE"])

        keys = pg.key.get_pressed()
        object_rects = [obj.rect for obj in map]

        player1.update(keys, object_rects)
        player1.draw(window)
        player2.update(keys, object_rects)
        player2.draw(window)

        for obj in map:
            obj.draw(vindu=window)
        pg.display.flip()
        clock.tick(FPS)

    pg.quit()

if __name__ == "__main__":
    main()