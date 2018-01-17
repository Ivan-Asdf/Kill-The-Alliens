import pygame, random, sys, time
from gol import GOL

class Ships():

    def __init__(self, bottomcenter_coords, sprites, sprites_expl, hp, speed, dmg, dmg_rate, dmg_speed, dmg_sprite, expl_time = 10):
        from main import screen
        self.screen = screen
        self.sprites = []
        self.sprites_expl = []
        for path in sprites:
            self.sprites.append(pygame.image.load(path))
        for path in sprites_expl:
            self.sprites_expl.append(pygame.image.load(path))
        self.sprite = self.sprites[0]
        self.rect = self.sprites[0].get_rect()
        self.rect.midbottom = bottomcenter_coords
        self.max_hp = hp
        self.hp = hp
        self.speed = speed
        self.dmg = dmg
        self.dmg_rate = dmg_rate
        self.dmg_speed = dmg_speed
        if dmg_sprite:
            self.dmg_sprite = pygame.image.load(dmg_sprite)
        self.destroyed = False
        # Other
        self.sprite_index = 0
        self.expl_time = expl_time
        self.expl_timer = len(self.sprites_expl)*self.expl_time

    def update(self):
        # Sprite to draw selection.
        #1 -IF Destroyed check
        if self.destroyed == True:
            if self.expl_timer >= len(self.sprites_expl)*self.expl_time:
                self.sprite_index = 0
                self.sprite = self.sprites_expl[self.sprite_index]
            elif self.expl_timer < (len(self.sprites_expl)-1-self.sprite_index)*self.expl_time:
                self.sprite_index +=1
                self.sprite = self.sprites_expl[self.sprite_index]
            elif self.expl_timer <=0:
                GOL.del_go(self)
            self.expl_timer -= 1
        #2 -If Alive dmg check
        elif self.hp <= self.max_hp*(len(self.sprites)-1-self.sprite_index)/len(self.sprites):
            self.sprite_index += 1
            self.sprite = self.sprites[self.sprite_index]

    def draw(self):
        self.screen.blit(self.sprite, self.rect)

    def take_dmg(self,dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.destroyed = True


class Aliens(Ships):
    
    def __init__(self, x, spawn_timer, sprites, sprites_expl, hp, speed, dmg, dmg_rate, dmg_speed, dmg_sprite):
        Ships.__init__(self, (x,0), sprites, sprites_expl, hp, speed, dmg, dmg_rate, dmg_speed, dmg_sprite)
        # Vertical coors
        self.y = float(self.rect.y)
        # Other
        self.dmg_timer = self.dmg_rate
        self.spawn_timer = spawn_timer
        self.spawned = False
    def update(self):
        if self.spawned:
            Ships.update(self)
            if not self.destroyed:
                # Movement
                self.y += self.speed
                self.rect.y = int(self.y)
                # Fire
                self.fire()
                # Check if reached bottom
                if self.rect.top == self.screen.get_rect().bottom:
                    GOL.get_go(Base).take_dmg(self.hp)
                    GOL.del_go(self)
        else:
            if self.spawn_timer <= 0:
                self.spawned = True
            else:
                self.spawn_timer -= 1

    def fire(self):
        if self.dmg_timer < 0:
            GOL.add_go(Projectile(self, "DOWN", self.dmg_speed, self.dmg, sprite=self.dmg_sprite, sprite_expl=r"images\alien\plasmaball_expl.png"))
            self.dmg_timer = self.dmg_rate
        else:
            self.dmg_timer -= 1

class Alien1(Aliens):

    def __init__(self, x,timer = 0):
        sprites = [r"images\alien\alien.png", r"images\alien\alien_dmg_2.png", r"images\alien\alien_dmg_3.png"]
        sprites_expl = [r"images\alien\alien_expl_1.png", r"images\alien\alien_expl_2.png", r"images\alien\alien_expl_3.png"]
        hp = 3
        speed = 0.5
        dmg = 1
        dmg_rate = 60*2
        dmg_speed = 5
        dmg_sprite = r"images\alien\plasmaball.png"
        Aliens. __init__(self, x, timer, sprites, sprites_expl, hp, speed, dmg, dmg_rate, dmg_speed, dmg_sprite)

class Alien2(Aliens):

    def __init__(self, x, timer = 0):
        sprites = [r"images\alien2\alien2.png", r"images\alien2\alien2_dmg_2.png", r"images\alien2\alien2_dmg_3.png"]
        sprites_expl = [r"images\alien2\alien2_expl_1.png", r"images\alien2\alien2_expl_2.png", r"images\alien2\alien2_expl_3.png"]
        hp = 9
        speed = 0.3
        dmg = 2
        dmg_rate = 60*4
        dmg_speed = 2
        dmg_sprite = r"images\alien2\alien2_plasmaball.png"
        Aliens.__init__(self, x, timer, sprites, sprites_expl, hp, speed, dmg, dmg_rate, dmg_speed, dmg_sprite)

    def fire(self):
        if self.dmg_timer < 0:
            GOL.add_go(Projectile(self, "DOWN", self.dmg_speed, self.dmg, sprite=self.dmg_sprite, sprite_expl=r"images\alien2\alien2_plasmaball_expl.png"))
            GOL.add_go(Projectile(self, (1,0.4), self.dmg_speed, self.dmg, sprite=self.dmg_sprite, sprite_expl=r"images\alien2\alien2_plasmaball_expl.png"))
            GOL.add_go(Projectile(self, (1,-0.4), self.dmg_speed, self.dmg, sprite=self.dmg_sprite, sprite_expl=r"images\alien2\alien2_plasmaball_expl.png"))
            self.dmg_timer = self.dmg_rate
        else:
            self.dmg_timer -= 1    


class Player(Ships):

    def __init__(self):
        sprites = [r"images\player\spaceship.png", r"images\player\spaceship_dmg_2.png", r"images\player\spaceship_dmg_3.png"]
        sprites_expl = [r"images\player\spaceship_expl_1.png", r"images\player\spaceship_expl_2.png", r"images\player\spaceship_expl_3.png"]
        hp = 10
        speed = 5
        dmg = 1
        dmg_rate = 60*0.25
        dmg_speed = 6
        dmg_sprite = r"images\player\bullet.png"
        Ships.__init__(self, (500,600-10), sprites, sprites_expl, hp, speed, dmg, dmg_rate, dmg_speed, dmg_sprite,expl_time=25)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.firing = False
        self.dmg_timer = self.dmg_rate
        self.shield_sprite = pygame.image.load(r"images\player\shield.png")
        self.shield_rect = self.shield_sprite.get_rect()
        self.shield_hp = 3
        self.shield_hp_max = self.shield_hp
        self.shield_charge = 0
        self.shield_charge_time = 60*5

    def update(self):
        Ships.update(self)
        self.check_collision()
        if not self.destroyed:
            # Movement
            if self.moving_right and self.rect.right < 1200:
                self.x += self.speed
            if self.moving_left and self.rect.left > 0:
                self.x -= self.speed
            if self.moving_up and self.rect.top > 0:
                self.y -= self.speed
            if self.moving_down and self.rect.bottom < 600:
                self.y += self.speed
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
            # Firing
            if self.firing and self.dmg_timer < 0:
                self.fire()
                self.dmg_timer = self.dmg_rate
            else:
                self.dmg_timer -= 1
            # Shield logic
            if self.shield_charge < self.shield_charge_time and self.shield_hp < self.shield_hp_max:
                self.shield_charge += 1
            if self.shield_charge >= self.shield_charge_time and self.shield_hp < self.shield_hp_max:
                self.shield_hp += 1
                self.shield_charge = 0

    def draw(self):
        Ships.draw(self)
        # Shield drawing
        if self.shield_hp > 0:
            self.screen.blit(self.shield_sprite, (self.rect.x - 2, self.rect.y -2))

    def fire(self):
        GOL.add_go(Projectile(self, "UP", self.dmg_speed, self.dmg,self.dmg_sprite))

    def take_dmg(self,dmg):
        if self.shield_hp > 0:
            self.shield_hp -= dmg
            self.shield_charge = 0
            if self.shield_hp < 0:
                self.hp += self.shield_hp
                self.shield_hp = 0
        else:
            self.hp -= dmg
            self.shield_charge = 0
        if self.hp <= 0:
            self.destroyed = True
            GOL.add_go(Title("GAME OVER!",60 , self.expl_time*3, color=(250,50,100)))

    def check_collision(self):
        for alien in GOL.get_golist(Aliens):
            if self.rect.colliderect(alien.rect) and alien.destroyed == False:
                alien.destroyed = True
                self.take_dmg(alien.hp)


class Projectile():

    def __init__(self, ship, dir, speed, dmg, sprite="", sprite_expl = r"images\player\bullet_expl.png"):
        from main import screen
        self.ship = ship
        self.screen = screen
        self.dir = dir
        # create rect
        if sprite:
            self.sprite = sprite
            self.rect = self.sprite.get_rect()
        else:
            self.rect = pygame.Rect(0, 0, 5, 10)
        # Spawn bullet on top of ship
        self.rect.centerx = ship.rect.centerx
        if dir == "UP": self.rect.bottom = ship.rect.top
        elif dir == "DOWN": self.rect.top = ship.rect.bottom
        elif isinstance(dir,tuple):
            self.rect.top = ship.rect.bottom
        self.y = float(self.rect.y) #float position
        self.x = float(self.rect.x)
        # Other attributes
        self.speed = speed
        self.dmg = dmg
        # Explosion related
        self.destroyed = False
        self.explosion_time = 10
        self.explosion_image = pygame.image.load(sprite_expl)

    def update(self):
        # while a solid bullet
        if not self.destroyed:
            # Move
            if self.dir == "UP":
                self.y -= self.speed
                self.rect.y = int(self.y)
            elif self.dir == "DOWN":
                self.y += self.speed
                self.rect.y = int(self.y)
            elif isinstance(self.dir, tuple):
                self.y += self.dir[0]*self.speed
                self.rect.y = int(self.y)
                self.x += self.dir[1]*self.speed
                self.rect.x = int(self.x)
            # Check if reach bottom or top
            if self.rect.top >= self.screen.get_rect().bottom:
                GOL.del_go(self)
            elif self.rect.bottom <= self.screen.get_rect().top:
                GOL.del_go(self)
            # Check if hit anything
            if isinstance(self.ship, Player):
                for alien in GOL.get_golist(Aliens):
                    if self.rect.colliderect(alien.rect):
                        if alien.spawned and not alien.destroyed:
                            alien.take_dmg(self.dmg)
                            self.destroyed = True
            elif isinstance(self.ship, Aliens):
                if GOL.get_go(Player):
                    if self.rect.colliderect(GOL.get_go(Player).rect):
                        GOL.get_go(Player).take_dmg(self.dmg)
                        self.destroyed = True

    def draw(self):
        if not self.destroyed:
            try:
                self.screen.blit(self.sprite, self.rect)
            except:
                pygame.draw.rect(self.screen, (250, 0, 0), self.rect)
        else:
            self.explode()

    def explode(self):
        """when destroyed"""
        self.explosion_time -= 1
        if self.explosion_time > 0:
            self.screen.blit(self.explosion_image, self.rect)
        else:
            GOL.del_go(self)


class PlayerInteface():

    class Bar():

        def __init__(self, width, height, thickness, leftspace, bottomspace, color, object, variable_name, icon = ""):
            from main import screen
            self.screen = screen
            self.width = width
            self.height = height
            self.var_height = height - thickness * 2
            self.thick = thickness
            self.leftspace = leftspace
            self.bottomspace = bottomspace
            self.color = color
            self.object = object
            self.variable_name = variable_name
            self.var_max_value = getattr(object, variable_name)
            # rectangle for collision (lazy :D)

            # Background surface (black bar behind the red hp bar)
            self.icon = icon
            if icon:
                self.icon_sprite = pygame.image.load(icon)
                self.icon_rect = self.icon_sprite.get_rect()
                self.bs = pygame.Surface((self.width, self.height + self.icon_rect.height))
                # self.bs.fill((35/2, 70/2, 123/2))
                self.bs.blit(self.icon_sprite, (0,0))
                self.rect = pygame.Rect((self.leftspace, 600 - self.bottomspace - self.height - self.icon_rect.height),
                                        (self.width, self.height + self.icon_rect.height))
            else:
                self.bs = pygame.Surface((self.width, self.height))
                self.rect = pygame.Rect((self.leftspace, 600 - self.bottomspace - self.height),
                                        (self.width, self.height))

            # Actual surface(color)
            self.s = pygame.Surface((self.width - self.thick * 2, self.var_height ))
            self.s.fill(self.color)
            # Other
            self.transparent = False

        def update(self):
            # Check collision
            self.transparent = False
            for object in GOL.get_golist():
                rect = getattr(object, "rect", "")
                if rect:
                    if self.rect.colliderect(rect):
                        self.transparent = True
            # Check variable
            # ! since a 0 height surface cant exist there is an IF statement
            if self.object and getattr(self.object, self.variable_name) > 0:
                self.var_height = getattr(self.object, self.variable_name) / self.var_max_value * (self.height - self.thick*2)
                self.s = pygame.Surface((self.width - self.thick * 2, self.var_height))
                self.s.fill(self.color)
                if self.transparent:
                    self.s.set_alpha(100)
                    self.bs.set_alpha(100)
                else:
                    self.s.set_alpha(250)
                    self.bs.set_alpha(250)

        def draw(self):
            # Background (black)
            if self.icon:
                self.screen.blit(self.bs, (self.leftspace, 600 - self.bottomspace - self.height - self.icon_rect.height))
            else:
                self.screen.blit(self.bs, (self.leftspace, 600 - self.bottomspace - self.height))
            # Foreground
            #! if there is no hp there is no hp bar(red) :D
            if self.object and getattr(self.object, self.variable_name) > 0:
                self.screen.blit(self.s, (self.leftspace + self.thick, 600 - self.bottomspace - self.var_height - self.thick))

    def __init__(self):
        self.hp_bar=self.Bar(30, 100, 1, 10, 10, (250, 0, 0), GOL.get_go(Player), "hp", icon=r"images\ui\hp_icon.png")
        self.shield_bar = self.Bar(30, 100, 1, 50, 10, (0, 100, 250), GOL.get_go(Player), "shield_hp", icon=r"images\ui\shield_icon.png")
        self.shield_charge_bar = self.Bar(10, 100, 1, 80, 10, (0, 200, 250), GOL.get_go(Player), "shield_charge", icon=r"images\ui\energy_icon.png")
        self.shield_charge_bar.var_max_value = 60 * 5
        self.base_hp = self.Bar(20, 100, 4, 100, 10, (250, 250, 0), GOL.get_go(Base), "hp",icon=r"images\ui\hq_icon.png")

    def update(self):
        self.hp_bar.update()
        self.shield_bar.update()
        self.shield_charge_bar.update()
        self.base_hp.update()

    def draw(self):
        self.hp_bar.draw()
        self.shield_bar.draw()
        self.shield_charge_bar.draw()
        self.base_hp.draw()

class Title():

    def __init__(self, text, font_size, time, color = (200, 250, 0)):
        from main import screen
        self.screen = screen
        self.time = time
        self.font = pygame.font.SysFont("Arial MS", size=font_size)
        self.text = self.font.render(text,True,color)
        self.rect = self.text.get_rect()
        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.centery = self.screen.get_rect().centery

    def update(self):
        self.time -= 1
        if self.time <= 0:
            GOL.del_go(self)

    def draw(self):
        self.screen.blit(self.text, self.rect)

class Base():

    def __init__(self):
        self.hp = 50

    def update(self):
        pass
    def draw(self):
        pass
    def take_dmg(self,dmg):
        self.hp -= dmg