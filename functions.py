import pygame, sys
from gol import GOL
from objects import *
from levels_manager import LM
clock = pygame.time.Clock()
# Backgound image
space = pygame.image.load(r"images\background\space.gif")

# User input
def check_event():
    for event in pygame.event.get():
        # Exit check
        if event.type == pygame.QUIT:
            sys.exit()
        # Ship movement
        if GOL.get_go(Player):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    GOL.get_go(Player).moving_right = True
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    GOL.get_go(Player).moving_left = True
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    GOL.get_go(Player).moving_up = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    GOL.get_go(Player).moving_down = True
                if event.key == pygame.K_SPACE:
                    GOL.get_go(Player).firing = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    GOL.get_go(Player).moving_right = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    GOL.get_go(Player).moving_left = False
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    GOL.get_go(Player).moving_up = False
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    GOL.get_go(Player).moving_down = False
                if event.key == pygame.K_SPACE:
                    GOL.get_go(Player).firing = False
# Game logic
def update():
    for object in GOL.get_golist():
        object.update()
# Rendering
def draw(screen):
    # Reset screen
    screen.blit(space,(0,0))
    # Object drawing
    for object in GOL.get_golist():
        object.draw()
    # Update and FPS
    font = pygame.font.SysFont("Arial MS", size=16)
    text = font.render(str(round(clock.get_fps(),2)),False, (250,250,250))
    screen.blit(text, (0, 0))
    pygame.display.flip()
    clock.tick(60)
# Initial setup
def setup():
    from main import screen
    # Delete old game objects
    GOL.del_golist()
    # Add new player, base, hp bars and reset levels
    GOL.add_go(Player())
    GOL.add_go(Base())
    GOL.add_go(PlayerInteface())
    LM.reset()
    gamestart = False

    while not gamestart:
        # Start screen, fill and text
        screen.fill((0, 250, 0))
        screen.blit(space,(0,0))
        pygame.font.init()
        font = pygame.font.SysFont("Tahoma MS", size=60)
        title = font.render("KILL ALL THE ALIENS!", True, (255, 215,0))
        rect = title.get_rect()
        rect.centerx = screen.get_rect().centerx
        rect.centery = screen.get_rect().top + 100
        screen.blit(title, rect)
        font = pygame.font.SysFont("Arial MS", size=18)
        title = font.render("PRESS ANY KEY TO START", True, (250, 250, 0))
        rect = title.get_rect()
        rect.centerx = screen.get_rect().centerx
        rect.centery = screen.get_rect().top + 400
        screen.blit(title, rect)

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                gamestart = True

def gameover():
    from main import screen
    pygame.font.init()
    font = pygame.font.SysFont("Arial MS", 50, bold=True)
    text_surface = font.render("GAME OVER", False, (250, 250, 0))
    screen.blit(text_surface,(500,300))




