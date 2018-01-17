# Kill-the-Aliens
SpaceInvader type game made using pygame library

## Requirements
Python 3.6  
pygame library  
#### Run main.py

## Controls
WASD or arrow keys - move   
SPACEBAR - shoot

## Notes
There are only 3 levels scripted by default in the level.json, more can be added.  
Cannot be compiled to exe using pyinstaller since the MS fonts used cant be loaded. If tried to be put inside directory and loaded using pygame.font.Font(r"filepath", size) there is an OSError.

