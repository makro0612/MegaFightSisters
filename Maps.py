from config import WINDOWHEIGHT,WINDOWWIDTH,colors

MAPS = {
    "basic": {
        "startpos":[(WINDOWWIDTH//2 - 250,WINDOWHEIGHT//2 + 180),(WINDOWWIDTH//2 + 250,WINDOWHEIGHT//2 + 180)],
        "objects": [
            (WINDOWWIDTH//2 - 600//2, WINDOWHEIGHT//2 + 200,600, 20, colors["RED"], False),
            (WINDOWWIDTH//2 - 350, WINDOWHEIGHT//2 + 120,100, 20, colors["RED"]),
            (WINDOWWIDTH//2 - 50, WINDOWHEIGHT//2 + 120,100, 20, colors["RED"]),
            (WINDOWWIDTH//2 + 250, WINDOWHEIGHT//2 + 120,100, 20, colors["RED"]),
            (WINDOWWIDTH//2 - 600//2, WINDOWHEIGHT//2 + 40,600, 20, colors["RED"]),]
        }
    }