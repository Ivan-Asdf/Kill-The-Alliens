import json
from gol import GOL
from objects import *
class LM():
    """Level Manager class"""
    lvl_num = 0
    levels = {
        "1":{
            "delay":3,
            "title":"LEVEL 1",
            "spawns":[
                {
                    "type":"alien1",
                    "x": 50,
                    "timer": 0,
                },
                {
                    "type": "alien1",
                    "x": 150,
                    "timer": 3,
                },
                {
                    "type": "alien2",
                    "x": 250,
                    "timer": 5,
                },
                {
                    "type": "alien1",
                    "x":800,
                    "timer": 1
                }

            ]
        },
        "2": {
            "delay": 3,
            "title": "LEVEL 2",
            "spawns": [
                {
                    "type": "alien2",
                    "x": 600,
                    "timer": 1,
                },
                {
                    "type": "alien2",
                    "x": 100,
                    "timer": 2,
                },
                {
                    "type": "alien2",
                    "x": 600-100,
                    "timer": 3,
                },

            ]
        },
        "3": {
            "delay": 3,
            "title": "LEVEL 3",
            "spawns": [
                {
                    "type": "alien2",
                    "x": 600,
                    "timer": 1
                },
                {
                    "type": "alien2",
                    "x": 100,
                    "timer": 2
                },
                {
                    "type": "alien2",
                    "x": 500,
                    "timer": 3
                },
                {
                    "type": "alien1",
                    "x": 100,
                    "timer": 3
                },
                {
                    "type": "alien1",
                    "x": 700,
                    "timer": 3
                },
                {
                    "type": "alien1",
                    "x": 1100,
                    "timer": 3
                }
            ]
        }
    }
    # Try to open levels.json if not use default setting previously initialised
    try:
        file = open("levels.json")
        levels = json.load(file)
    except:
        file = open("levels.json","w")
        json.dump(levels, file, indent=4)

    @classmethod
    def update(cls):
        from main import screen
        cls.screen = screen
        if cls.lvl_ended() and cls.lvl_num < len(cls.levels):
            cls.lvl_num += 1
            cls.play_lvl(cls.lvl_num)

    @classmethod
    def lvl_ended(cls):
        for x in GOL.get_golist():
            if isinstance(x,Aliens):
                return False
        return True

    @classmethod
    def play_lvl(cls,lvl_num):
        lvl = cls.levels[str(lvl_num)]
        GOL.add_go(Title(lvl["title"], 100, 60*lvl["delay"]))
        for spawn in lvl["spawns"]:
            if spawn["type"] == "alien1":
                GOL.add_go(Alien1(spawn["x"], timer=spawn["timer"]*60+lvl["delay"]*60))
            if spawn["type"] == "alien2":
                GOL.add_go(Alien2(spawn["x"], timer=spawn["timer"]*60+lvl["delay"]*60))

    @classmethod
    def reset(cls):
        cls.lvl_num = 0

