# Libraries
# Other project modules
from functions import *
from objects import *
from gol import GOL
from levels_manager import LM
# Initial stuff
pygame.init()
# Window
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("KILL THE ALIENS!!")

# Mainloop
while True:
    gameover = False
    setup()
    while not gameover:
        LM.update()
        check_event()
        update()
        draw(screen)
        gameover = True
        for x in GOL.golist:
            if isinstance(x, Player):
                gameover = False










