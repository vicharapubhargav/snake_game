import collections

import pygame
import random
from pygame import Rect
from pygame.math import Vector2

# Global Variables
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

spacing = (12, 0)

GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

pygame.init()

# colors
c1,c2,c3 = (107,142,35),(173, 245, 66),(66, 245, 215)
snakeColors = [c1,c2,c3]

FPS = 7

CENTER = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

STOP = (0, 0)

system_time = pygame.time.get_ticks()
shielding_time = 0
loc_time=0
multiplierfood_time =0
superfood_choice=1
foodPos = (0, 0)
multiplierfood_pos=(0,0)

highScoreSurface = pygame.Surface((GRID_WIDTH * 15.5, GRID_HEIGHT * 16))

startGame = True
running = True
endGame = False
border = True

player = ''

pn_bg = Rect(GRID_WIDTH * 7.6, GRID_HEIGHT * 20.85, 180, 30)
rg_bg = Rect(GRID_WIDTH * 1.25, GRID_HEIGHT * 24.0, 120, 50)
sg_bg = Rect(GRID_WIDTH * 3, GRID_HEIGHT * 25.4, 250, 50)
eg_bg = Rect(GRID_WIDTH * 10.5, GRID_HEIGHT * 24.0, 120, 50)

top10HighScores = {}
player_name_bg_color = (255, 255, 255)
isBorderOn = False

screen = pygame.display.set_mode((SCREEN_WIDTH + spacing[0] * GRID_SIZE, SCREEN_HEIGHT + spacing[1] * GRID_SIZE))

title = pygame.font.Font('arial.ttf', 35)
heading1 = pygame.font.Font('arial.ttf', 25)
heading3 = pygame.font.Font('arial.ttf', 20)
paragraph = pygame.font.Font('arial.ttf', 16)
monospace = pygame.font.SysFont("monospace", 17)

FoodImage = pygame.image.load("meat.png").convert_alpha()
apple = pygame.image.load("apple.png").convert_alpha()


class Snake:
    def __init__(self):
        self.length = 3
        self.score = 0
        self.color_choice=0
        self.positions = [(CENTER[0] - 2 * GRID_SIZE, CENTER[1]), (CENTER[0] - GRID_SIZE, CENTER[1]), CENTER]
        self.direction = RIGHT
        self.color = pygame.Color(c1)
        self.outline_color = pygame.Color("slategrey")

    def get_head_position(self):
        return self.positions[0]

    def turn(self, new_dir):
        if self.length > 1 and (new_dir[0] * -1, new_dir[1] * -1) == self.direction:
            return
        else:
            self.direction = new_dir

    def move(self):
        global isBorderOn
        temp = 0
        cur = self.get_head_position()
        x, y = self.direction
        new_pos = ((cur[0] + (x * GRID_SIZE)), cur[1] + (y * GRID_SIZE))
        if new_pos[0] < 0:
            new_pos = (((GRID_WIDTH - 1) * GRID_SIZE), cur[1] + (y * GRID_SIZE))
            isBorderOn = True
            temp = 1
        elif new_pos[1] < 0:
            new_pos = ((cur[0] + (x * GRID_SIZE)), ((GRID_HEIGHT - 1) * GRID_SIZE))
            isBorderOn = True
            temp = 3
        elif new_pos[1] >= SCREEN_HEIGHT:
            new_pos = ((cur[0] + (x * GRID_SIZE)), 0)
            isBorderOn = True
            temp = 4
        elif new_pos[0] >= SCREEN_WIDTH:
            new_pos = (0, cur[1] + (y * GRID_SIZE))
            isBorderOn = True
            temp = 2

        if isBorderOn and border:
            print(temp)
            self.die()
        elif len(self.positions) > 2 and new_pos in self.positions[2:]:
            print("6")
            self.die()
        else:
            self.positions.insert(0, new_pos)
            if len(self.positions) > self.length:
                self.positions.pop()
        isBorderOn = False

    def die(self):
        global system_time, shielding_time, endGame, border, multiplierfood_time,loc_time

        if not endGame:
            score_file_text = ''
            scores_file = open("High_Scores.txt", "wt")

            if top10HighScores.get(player.lower(), -1) == -1:
                top10HighScores[player.lower()] = self.score
            else:
                if self.score > top10HighScores[player.lower()]:
                    top10HighScores[player.lower()] = self.score

            sort_dict = sorted(top10HighScores.items(), key=lambda kv: kv[1])
            sort_dict.reverse()
            sorted_dict = collections.OrderedDict(sort_dict)

            count = 0
            for x in sorted_dict.keys():
                score_file_text += str(x) + ' - ' + str(sorted_dict[str(x)]) + '\n'
                count += 1
                if count > 9:
                    break
            scores_file.write(score_file_text)
            scores_file.close()

        self.length = 3
        self.positions = [(CENTER[0] - 2 * GRID_SIZE, CENTER[1]), (CENTER[0] - GRID_SIZE, CENTER[1]), CENTER]
        self.direction = STOP
        self.score = 0
        border = False
        system_time = pygame.time.get_ticks()
        shielding_time = pygame.time.get_ticks()
        multiplierfood_time = 0
        self.color = pygame.Color(c1)
        endGame = True
        #loc_time=0
        
        

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0] + spacing[0] * GRID_SIZE, p[1] + spacing[1] * GRID_SIZE),
                            (GRID_SIZE-3, GRID_SIZE-3))
            pygame.draw.ellipse(surface, self.color, r)
            

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.mposition = (0,0)
        self.color_choice = c1
        self.outline_color = pygame.Color("slategrey")
        self.randomize_position()
        self.randomize_multiFood()
        self.multiplierfood= False
        self.superfoodchoice=1

    def randomize_position(self):
        rand_x = random.randint(0, int(GRID_WIDTH - 1))
        rand_y = random.randint(0, int(GRID_HEIGHT - 1))
        self.position = (rand_x * GRID_SIZE, rand_y * GRID_SIZE)
        global foodPos
        foodPos = self.position
        

    def randomize_multiFood(self):
        rand_x = random.randint(0, int(GRID_WIDTH - 1))
        rand_y = random.randint(0, int(GRID_HEIGHT - 1))
        self.mposition = (rand_x * GRID_SIZE, rand_y * GRID_SIZE)
        global multiplierfood_pos
        multiplierfood_pos=self.mposition
        

    def draw_multifood(self, surface):
        r = pygame.Rect((self.mposition[0] + (spacing[0] * GRID_SIZE), self.mposition[1] + (spacing[1] * GRID_SIZE))
            , (GRID_SIZE, GRID_SIZE))
        if self.superfoodchoice==1:
            surface.blit(FoodImage,r)
        else:
            pygame.draw.rect(surface, self.color_choice, r)
            #pygame.draw.rect(surface, self.outline_color, r, 1)
    
       
    def draw(self, surface):
        if self.multiplierfood:
            self.draw_multifood(surface)
        
        r = pygame.Rect((self.position[0] + (spacing[0] * GRID_SIZE), self.position[1] + (spacing[1] * GRID_SIZE))
                        , (GRID_SIZE, GRID_SIZE))
        
        surface.blit(apple,r)
        #pygame.draw.rect(surface, self.color, r)
        #pygame.draw.rect(surface, self.outline_color, r, 1)


def display_high_score(surface, main_surface):
   pass

def left_panel(surface):
    pass


class World:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()

    def update(self):
        global system_time, shielding_time, multiplierfood_time,loc_time
        loc_time = pygame.time.get_ticks()
        self.snake.move()
        if self.snake.get_head_position() == self.food.mposition and self.food.multiplierfood:
            if  self.food.superfoodchoice==1:
                self.snake.length += 1
                self.snake.score += 2
            elif self.food.superfoodchoice==2:
                self.snake.color = self.food.color_choice

            self.food.multiplierfood= False
            for block in self.snake.positions[1:]:
                if block == self.food.position:
                    self.food.randomize_multiFood()
                
        if self.snake.get_head_position() == self.food.position:
            self.snake.length += 1
            self.snake.score += 1
            self.food.randomize_position()
            for block in self.snake.positions[1:]:
                if block == self.food.position:
                    self.food.randomize_position()

        
    def draw(self, surface):
        global shielding_time, border , multiplierfood_time, loc_time
        
       
        if system_time - shielding_time > 9000:
            shielding_time = system_time
            border = not border

        if loc_time - multiplierfood_time > random.randint(8,10) * 1000:
            choice = random.randint(1,2)
            self.food.multiplierfood = not self.food.multiplierfood
            multiplierfood_time = loc_time
            self.food.superfoodchoice=choice
                
            if choice==2:
                temp = snakeColors.copy()
                print(self.snake.color)
                temp.remove(self.snake.color)
                self.food.color_choice = temp[random.randint(0,1)]
                
            self.food.randomize_multiFood()
                
        if (self.food.multiplierfood) and (loc_time - multiplierfood_time >= 8000 ):
            self.food.multiplierfood = False
            
        if border:
            self.snake.draw(surface)
            self.food.draw(surface)
           
            pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(spacing[0] * GRID_SIZE,
                                                             spacing[1] * GRID_SIZE,
                                                             SCREEN_WIDTH, SCREEN_HEIGHT), 3)
        else:
            self.snake.draw(surface)
            self.food.draw(surface)


    def score(self):
        return self.snake.score

    def handle_keys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.turn(UP)
            elif event.key == pygame.K_DOWN:
                self.snake.turn(DOWN)
            elif event.key == pygame.K_LEFT:
                self.snake.turn(LEFT)
            elif event.key == pygame.K_RIGHT:
                self.snake.turn(RIGHT)


def draw_grid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect(((x + spacing[0]) * GRID_SIZE, (y + spacing[1]) * GRID_SIZE),
                                (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, pygame.Color("lightslategrey"), r)
            else:
                r = pygame.Rect(((x + spacing[0]) * GRID_SIZE, (y + spacing[1]) * GRID_SIZE),
                                (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, pygame.Color("slategrey"), r)


def run():
    global system_time, running, endGame, startGame, player, player_name_bg_color, world
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake Pygame Example")

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    world = World()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif startGame:
                    if event.key == pygame.K_BACKSPACE:
                        player = player[:-1]
                        player_name_bg_color = (255, 255, 255)
                    elif event.key == pygame.K_RETURN:
                        pass
                    else:
                        player += event.unicode
                        player_name_bg_color = (255, 255, 255)
                else:
                    world.handle_keys(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sg_bg.collidepoint(event.pos):
                    if len(player.strip()) > 0:
                        running = True
                        startGame = False
                    else:
                        player_name_bg_color = (255, 0, 0)
                elif eg_bg.collidepoint(event.pos):
                    print("Quit")
                    running = False
                elif rg_bg.collidepoint(event.pos):
                    print("Restart")
                    world.snake.direction = RIGHT
                    world.food.randomize_position()
                    world.food.multiplierfood = False
                    endGame = False
                    running = True
                    startGame = False
         

        surface.fill("slategrey")
        draw_grid(surface)

        if endGame:
            world.food.multiplierfood = False
            pygame.draw.rect(surface, (80, 120, 244), rg_bg)
            pygame.draw.rect(surface, (255, 155, 148), eg_bg)

            player_name_lbl = heading3.render('Restart', True, (0, 0, 0))
            player_name_lbl_rect = player_name_lbl.get_rect(
                topleft=(GRID_WIDTH * 2.55, GRID_HEIGHT * 24.65))
            surface.blit(player_name_lbl, player_name_lbl_rect)

            end_name_lbl = heading3.render('Quit', True, (0, 0, 0))
            end_name_lbl_rect = end_name_lbl.get_rect(
                topleft=(GRID_WIDTH * 12.5, GRID_HEIGHT * 24.65))
            surface.blit(end_name_lbl, end_name_lbl_rect)
        elif not startGame:
            world.update()
            world.draw(surface)
        left_panel(surface)
        screen.blit(surface, (0, 0))

        text = heading3.render("Shield " + "{:.1f}"
                               .format((system_time - shielding_time)/1000), True, pygame.Color("black"))
        if not startGame and not endGame:
            screen.blit(text, (860, 15))

        text = heading3.render("Score: {0}".format(world.score()), True, pygame.Color("black"))
        screen.blit(text, (365, 15))
        system_time = pygame.time.get_ticks()

        pygame.display.update()


world = World()

if __name__ == '__main__':
    run()
    pygame.quit()
