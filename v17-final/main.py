### >>> Imports:

import pygame as pg
import random

from settings import *
# >>> Issue with classes not importing under *, so they are imported manually. -__-
# Head that is controlled by the player:
from sprites import Player
# Walls that when collided with end the game:
from sprites import Wall

from sprites import Medal

### >>> Game Loop
class Game():

    # >>> Initialize Program (When game is first opened):
    def __init__(self):
        
        # Initialize Pygame.
        pg.init()

        # Create the window for the game, under a variable named "screen":
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # Set the name that displays at the top of the window:
        pg.display.set_caption(TITLE)

        # Create a clock for the game:
        # This will later handle the speed/FPS of the game.
        self.clock = pg.time.Clock()

        # Set up custom event to move the snake:
        self.MOVESNAKE = pg.USEREVENT + 1
        # Set up timer to trigger snake movement every # milliseconds:
        pg.time.set_timer(self.MOVESNAKE, 250)

        # Initialize variable "running", and set to true.
        self.running = True

        # self.show_a_menu_screen = False
        self.show_go_screen = False

        self.font = pg.font.Font(os.path.join(font_folder, "Ac437_ToshibaSat_8x8.ttf"), 32)

    # >>> Initialize Game (Whenever a new game is started):
    def new(self):

        # Create a new group to hold all of our sprites:
        # We can use this to mass-update sprites in our Game Loop updates.
        self.all_sprites = pg.sprite.Group()

        # Create a group to hold all of our walls:
        self.walls = pg.sprite.Group()
        # Create a group for food (should only contain one item at a time, though):
        self.food = pg.sprite.Group()
        # Create a group to hold all of our snake segments (including the head):
        self.snake = pg.sprite.Group()

        self.medals = pg.sprite.Group()

        # Initialize player at grid coordinates:
        self.player = Player(self, 4, 4)
        # Set player starting direction:
        self.direction = "right"

        # Spawn our walls:
        # Spawn walls along x axis:
        for x in range(0, 13, 1):
            Wall(self, x, 0)
            Wall(self, x, 12)
        # Spawn walls along y axis:
        for y in range(0, 13, 1):
            Wall(self, 0, y)
            Wall(self, 12, y)

        # Other than that, when a new game starts... Run it:
        self.run()

    # >>> Run Game (Main Game Loop):
    def run(self):
        # Initialize variable "playing" and set it to true.
        # Different than "running" which just indicates the program is running.
        self.playing = True

        # Then use that to control the activity of the game loop:
        while self.playing:

            # Keep loop running at the right speed:
            # The loop runs really fast, so this will pause operations until the % of a second we specify has passed.
            self.clock.tick(FPS)

            # Run events:
            self.events()
            # Run updates:
            self.update()
            # Run drawing / rendering:
            self.draw()
        self.game_over_screen()

    # >>> Function that runs when the game ends:
    def game_over_screen(self):
        # Get final score:
        self.final_score = str(len(self.snake.sprites()) - 3)
        # Show GO screen:
        self.show_a_menu_screen = True
        self.show_go_screen = True

        if int(self.final_score) < 20:
            self.medal_id = "na"
        elif int(self.final_score) < 45:
            self.medal_id = "bronze"
        elif int(self.final_score) < 70:
            self.medal_id = "silver"
        elif int(self.final_score) < 115:
            self.medal_id = "gold"
        elif int(self.final_score) >= 115:
            self.medal_id = "platinum"

        self.medal = Medal(self, self.medal_id)

        while self.show_go_screen:
            # Run events:
            self.events()
            self.draw()

    # >>> Function that runs when the game first opens:  
    def game_start_screen(self):
        self.show_a_menu_screen = True
        self.show_start_screen = True

        while self.show_start_screen:
            # Run events:
            self.events()
            self.draw()

        game.new()
        return

    # >>> Process Input:
    def events(self):
    
        # For every event pygame picks up:
        for event in pg.event.get():

            # Check if the event was "closing the game window":
            if event.type == pg.QUIT:
                pg.quit()
                # Kill program loop.

            # Check if the event was "pressing a key":
            if event.type == pg.KEYDOWN:
                # And if so, was it pressing an arrow key?
                # If an arrow key was pressed, change the player's head's movement direction:
                # Don't let them turn right around though! That's not how snake works!
                if not self.show_a_menu_screen:
                    if event.key == pg.K_LEFT and self.direction != "right":
                        self.direction = "left"
                    if event.key == pg.K_RIGHT and self.direction != "left":
                        self.direction = "right"
                    if event.key == pg.K_UP and self.direction != "down":
                        self.direction = "up"
                    if event.key == pg.K_DOWN and self.direction != "up":
                        self.direction = "down"

                if event.key == pg.K_y and self.show_a_menu_screen:
                    self.show_go_screen = False
                    self.show_start_screen = False
                    self.show_a_menu_screen = False
                    self.new()
                    

            # Check if the event was "move the snake":
            # If so, call move on the snake's head, then flip the sprite correctly.
            if event.type == self.MOVESNAKE and not self.show_a_menu_screen:
                if self.direction == "left":
                    self.player.move(dx=-1)
                if self.direction == "right":
                    self.player.move(dx=1)
                if self.direction == "up":
                    self.player.move(dy=-1)
                if self.direction == "down":
                    self.player.move(dy=1)
                self.player.flip_sprite(self.direction)
     
    # >>> Update Game:
    def update(self):

        # Update all the sprites in our sprite group:
        self.all_sprites.update()

    # >>> Draw Tile Grid, Called in draw():
    def draw_grid(self):

        # Draw horizontal grid lines:
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, BLUE, (x, 0), (x, HEIGHT))
        # Draw vertical grid lines:
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, BLUE, (0, y), (WIDTH, y))

    # >>> Draw / Render Game:
    def draw(self):

        if not self.show_a_menu_screen:
        # Fill the screen with white (as a background) each frame, to overwrite the previous frame:
            self.screen.fill(WHITE)

            # Draw a grid on the screen to visualize tiles:
            # self.draw_grid()

            # Draw all the sprites in our sprite group (onto the screen):
            self.all_sprites.draw(self.screen)

            # Draw the snake on top!
            self.snake.draw(self.screen)

            self.font = pg.font.Font(os.path.join(font_folder, "Ac437_ToshibaSat_8x8.ttf"), 32)
            self.textSufaceObj = self.font.render("Score:" + str(len(self.snake.sprites()) - 3), True, WHITE, None)
            self.screen.blit(self.textSufaceObj, (16, 16))
        elif self.show_a_menu_screen and self.show_go_screen:
            # If you GO'd
            self.screen.fill(WALLBLACK)

            self.medals.draw(self.screen)

            self.go_text_1 = self.font.render("Game Over!", True, WHITE, None)
            self.go_text_2 = self.font.render("You scored: " + self.final_score + " point(s)!", True, WHITE, None)

            if self.medal_id == "na":
                self.go_text_3 = self.font.render("...That's too low for a medal.", True, WHITE, None)
            else: 
                self.go_text_3 = self.font.render("...And earned a " + self.medal_id + " medal:", True, WHITE, None)

    
            self.go_text_4 = self.font.render("!", True, WHITE, None)
            self.go_text_5 = self.font.render("Press \"y\" to play again!", True, WHITE, None)
            self.go_text_6 = self.font.render("Or don't! I'm not your boss!", True, WHITE, None)


            self.screen.blit(self.go_text_1, (16, 16))
            self.screen.blit(self.go_text_2, (16, 64))
            self.screen.blit(self.go_text_3, (16, 112))

            if self.medal_id == "na":
                self.screen.blit(self.go_text_5, (16, 240))
                self.screen.blit(self.go_text_6, (16, 288))
            else:
                self.screen.blit(self.go_text_4, (104, 194))
                self.screen.blit(self.go_text_5, (16, 248))
                self.screen.blit(self.go_text_6, (16, 296))



        else:
            self.screen.fill(WALLBLACK)
            self.font = pg.font.Font(os.path.join(font_folder, "Ac437_ToshibaSat_8x8.ttf"), 32)
            self.gs_text_1 = self.font.render("Welcome to", True, WHITE, None)
            self.gs_text_2 = self.font.render("SNAKE BUT GOOD", True, RED, None)
            self.gs_text_3 = self.font.render("Press 'y' to play!", True, WHITE, None)
            self.screen.blit(self.gs_text_1, (16, 16))
            self.screen.blit(self.gs_text_2, (16, 64))
            self.screen.blit(self.gs_text_3, (16, 112))

        # Use Double Buffering:
        # I don't entirely understand it, but it makes rendering less taxing.
        # Always have this be AFTER you've drawn everything to the screen.
        pg.display.flip()

### >>> Run Game Loop:
        
# Store our Game() class inside a variable: 
game = Game()

while game.running:

    # Start a new game:
    game.game_start_screen()

# When the game loop has ended, quit.
# Also always quits when you try to close the window.
pg.quit()