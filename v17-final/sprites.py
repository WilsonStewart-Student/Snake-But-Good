### >>> Imports:

import pygame as pg
import random 
import os

from settings import *

### >>> Player Sprite:
class Player(pg.sprite.Sprite):
    # >>> Initialize Player:
    # >>> Player is initialized over in Game in main.py. It accepts an argument for the game class, and its starting X and Y postions (gridwise).
    # >>> Player accounts for the snake's head, but not body, due to how they behave.
    def __init__(self, game, x, y):

        # Add the sprite to our all_sprites group, and the snake group.
        self.groups = game.all_sprites, game.snake

        # Run Pygame's sprite initialization function:
        pg.sprite.Sprite.__init__(self, self.groups)

        # Set self.game to the Game class.
        self.game = game

        # Spawn first food item:
        self.food = Food(game, random.randint(5, 11), random.randint(5, 11))

        # Give the sprite its image (the snake head):
        self.image = pg.image.load(os.path.join(sprites_folder, "head-right.png")).convert()
        # Set the image to the desired size/dimensions:
        self.image = pg.transform.scale(self.image,(TILESIZE, TILESIZE))
        # Make any WHITE parts of the image transparent (pygame doesn't automatically respect transparency):
        self.image.set_colorkey(BLACK)

        # Give the sprite a surrounding rectangle (helps define where our sprite is in physical space):
        # In this case, we can just use get_rect() to make one that perfectly fits around the dimensions of our surface. :D
        self.rect = self.image.get_rect()

        # Get the coordinates the player is to initialize at, given to us in Game:
        self.x = x
        self.y = y

        # Give self a snake_segment_id of 1. The head is always 1, other parts will be set to the current length of the "snake" spritegroup.
        self.snake_segment_id = 1

        # Create a lists to hold snake segment locations before movement:
        self.snake_segment_locations_x = []
        self.snake_segment_locations_y = []

        # Determine if snake can move (yes to begin with!):
        self.can_move = True;
    
        # Make the snake not just a head to begin with:
        self.body_segment = Player_Body(self, self.game, 3, 4)
        self.body_segment = Player_Body(self, self.game, 2, 4)

    # >>> Player Move Function:
    # dx is how much the player should move on the x axis, and dy on the y axis.
    # They are 0 here, so that is their DEFAULT value.
    def move(self, dx=0, dy=0):
        # If the  player is not colliding with a wall by taking their next movement, move.
        if not self.collide_with_walls(dx, dy) and self.can_move:
            # Store where you just were (for the successive segment to follow):
            self.old_x = self.x
            self.old_y = self.y
            
            # Put those stored coordinates into the segment location list.
            if len(self.snake_segment_locations_x) != 0:
                self.snake_segment_locations_x[0] = self.old_x
                self.snake_segment_locations_y[0] = self.old_y
            else:
                self.snake_segment_locations_x.insert(0, self.old_x)
                self.snake_segment_locations_y.insert(0, self.old_y)

            # Then change location (movement actually applied in update.)
            self.x += dx
            self.y += dy

            # Then move segments:
            for x in range (len(self.game.snake.sprites())):
                if x > 0:
                    self.game.snake.sprites()[x].move()

        elif self.collide_with_walls(dx, dy):
            # Fix: This needs to trigger something in main/Game.
            if self.can_move:
                print("Game Over!")
            self.can_move = False
            self.game.playing = False

        if self.collide_with_food():
            # Kill food:
            Food.get_eaten(self.food)
            # Respawn food in new location:
            self.food_spawn_point_x = random.randint(1, 11)
            self.food_spawn_point_y = random.randint(1, 11)
            spawn_food = self.find_free_spawnpoint()
            while spawn_food == False:
                self.food_spawn_point_x = random.randint(1, 11)
                self.food_spawn_point_y = random.randint(1, 11)
                spawn_food = self.find_free_spawnpoint()
            
            self.food = Food(self.game, self.spawn_coordinates[0], self.spawn_coordinates[1])
            self.body_segment = Player_Body(self, self.game, self.old_x, self.old_y)


    # >>> Detect if Player Colliding With Walls:
    def collide_with_walls(self, dx=0, dy=0):
        # For each wall that exists in our walls group:
        for wall in self.game.walls:
            # Check if the location of that wall is the location the player is trying to move to:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                # And if so, return True:
                return True
        # Also check for running into self:
            for x in range (len(self.game.snake.sprites())):
                if x > 0:
                    if self.game.snake.sprites()[x].x == self.x + dx and self.game.snake.sprites()[x].y == self.y + dy:
                        return True
        return False
    
    # >>> Detect if Player Colliding With Food:
    def collide_with_food(self):

        if self.food.x == self.x and self.food.y == self.y:
                # And if so, return True:
                return True
        # If not, return false:
        return False
    
    # >>> Find free spot to spawn food:
    def find_free_spawnpoint(self):

        self.spawn_coordinates = [self.food_spawn_point_x, self.food_spawn_point_y]
        
        for i in range(len(self.snake_segment_locations_x)):
            if self.food_spawn_point_x == self.snake_segment_locations_x[i] and self.food_spawn_point_y == self.snake_segment_locations_y[i] or self.food_spawn_point_x == self.x and self.food_spawn_point_y == self.y:
                return False
        return True
            
    # >>> Player Sprite Flip Function:
    def flip_sprite(self, direction):
        if self.can_move:
            if direction == "left":
                self.image = pg.image.load(os.path.join(sprites_folder, "head-left.png")).convert()
            if direction == "right":
                self.image = pg.image.load(os.path.join(sprites_folder, "head-right.png")).convert()
            if direction == "up":
                self.image = pg.image.load(os.path.join(sprites_folder, "head-up.png")).convert()
            if direction == "down":
                self.image = pg.image.load(os.path.join(sprites_folder, "head-down.png")).convert()
            self.fix_sprite()

    # >>> Fix up sprite so there are no weird visual errors after being changed.
    def fix_sprite(self):
        # Set the image to the desired size/dimensions:
        self.image = pg.transform.scale(self.image,(TILESIZE, TILESIZE))
        # Make any BLACK parts of the image transparent (pygame doesn't automatically respect transparency):
        self.image.set_colorkey(BLACK)

    # >>> Set Player Update Behavior:
    def update(self):

        # Take the grid coordinates stored in self.x/y, turn them into pixel coordinates, and apply them to our rect.
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


### >>> Player Body Sprite:
class Player_Body(pg.sprite.Sprite):

    # >>> Initialize Snake Body:
    def __init__(self, player, game, x, y):
        # Add the sprite to our all_sprites group, and the snake group.
        self.groups = game.all_sprites, game.snake

        # Run Pygame's sprite initialization function:
        pg.sprite.Sprite.__init__(self, self.groups)

        # Set self.game to the Game class:
        self.game = game

        # Set self.player to the Game class:
        self.player = player

        # Set up sprite and rect:   
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(SNAKEGREEN)
        self.rect = self.image.get_rect()

        # Give self a snake_segment_id, equal to the current length of the snake with this segment.
        self.snake_segment_id = len(self.game.snake.sprites())

        # Set x and y to initially passed x and y.
        self.x = x
        self.y = y

    def move(self):
        
        # Store current coordinates in old_xy:
        self.old_x = self.x
        self.old_y = self.y

        # Put those stored coordinates into the segment location list.
        if len(self.player.snake_segment_locations_x) <= (self.snake_segment_id - 1):
            self.player.snake_segment_locations_x.insert(self.snake_segment_id - 1, self.old_x)
            self.player.snake_segment_locations_y.insert(self.snake_segment_id - 1, self.old_y)
        else:
            self.player.snake_segment_locations_x[self.snake_segment_id - 1] = self.old_x
            self.player.snake_segment_locations_y[self.snake_segment_id - 1] = self.old_y

        self.x = self.player.snake_segment_locations_x[self.snake_segment_id - 2]
        self.y = self.player.snake_segment_locations_y[self.snake_segment_id - 2]

    def update(self):

        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE



### >>> Food Sprite:
class Food(pg.sprite.Sprite):
    # >>> Initialize Food:
    # >>> Food is initialized over in Game in main.py. It accepts an argument for the game class, and its starting X and Y postions (gridwise).
    def __init__(self, game, x, y):
        
        self.game = game

        # Add the sprite to our all_sprites group, and to a "food" group:
        self.groups = game.all_sprites, game.food

        # Run Pygame's sprite initialization function:
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = pg.image.load(os.path.join(sprites_folder, "food.png")).convert()
        # Set the image to the desired size/dimensions:
        self.image = pg.transform.scale(self.image,(TILESIZE, TILESIZE))
        # Make any BLACK parts of the image transparent (pygame doesn't automatically respect transparency):
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

        # Apply our initially passed x and y location.
        self.x = x
        self.y = y

        # Since this sprite doesn't move after being initialized, convert from grid xy to pixel xy in init:
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def get_eaten(self):
        self.kill()



### >>> Wall Sprite:
class Wall(pg.sprite.Sprite):

    # >>> Initialize Wall:
    def __init__(self, game, x, y):
        # Add the sprite to our all_sprites group, and to a "walls" group:
        self.groups = game.all_sprites, game.walls

        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WALLBLACK)

        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE



###>>> Medal Sprite
class Medal(pg.sprite.Sprite):
    def __init__(self, game, color):
        # Add the sprite to our all_sprites group, and to a "walls" group:

        self.groups = game.all_sprites, game.medals

        self.game = game
        self.color = color

        pg.sprite.Sprite.__init__(self, self.groups)
        
        if self.color == "na":
            self.image = pg.image.load(os.path.join(sprites_folder, "blank.png")).convert()
        if self.color == "bronze":
            self.image = pg.image.load(os.path.join(sprites_folder, "bronze.png")).convert()
        elif self.color == "silver":
            self.image = pg.image.load(os.path.join(sprites_folder, "silver.png")).convert()
        elif self.color == "gold":
            self.image = pg.image.load(os.path.join(sprites_folder, "gold.png")).convert()
        elif self.color == "platinum":
            self.image = pg.image.load(os.path.join(sprites_folder, "platinum.png")).convert()

        self.image.set_colorkey(BLACK)

        # Set the image to the desired size/dimensions:
        self.image = pg.transform.scale(self.image,(96, 96))

        self.rect = self.image.get_rect()

        self.rect.x = 16
        self.rect.y = 144

        print("pee")
