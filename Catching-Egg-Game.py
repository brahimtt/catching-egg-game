import random
import pygame
import time
from tkinter import messagebox
import tkinter as tk
from pygame.locals import *

pygame.init()

#set the screen size 
screen_width= 800
screen_height= 600
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('basket game')
main_menu = False
font = pygame.font.Font('freesansbold.ttf', 24)
menu_command = 0
#set the colors
black=(0,0,0)
white=(255,255,255)
gray=(128,128,128)
# Set initial score to zero
gameover=False
score = 0
misses=0

# Create the Tkinter root window
root = tk.Tk()
root.withdraw()
#load the music for game 
pygame.mixer.music.load("chickenSound.mp3")
pygame.mixer.music.play()
#class for buttons 
class Button:
    def __init__(self, txt, pos):
        self.text = txt
        self.pos = pos
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (260, 40))

    def draw(self):
        pygame.draw.rect(screen, 'light gray', self.button, 0, 5)
        pygame.draw.rect(screen, 'dark gray', [self.pos[0], self.pos[1], 260, 40], 5, 5)
        text2 = font.render(self.text, True, 'black')
        screen.blit(text2, (self.pos[0] + 15, self.pos[1] + 7))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False
# Class for the basket
class Basket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load the basket image
        self.image = pygame.transform.scale(pygame.image.load("bowl.png"),(80,50))
        self.rect = self.image.get_rect()
        

        # Set the initial position of the basket
        self.rect.x = screen_width // 2 - self.rect.width // 2
        self.rect.y = screen_height - self.rect.height

    def update(self, direction):
        # Move the basket based on the direction
        if direction == "left":
            self.rect.move_ip(-7,0)
        elif direction == "right":
            self.rect.move_ip(7,0)

        # Limit the basket movement within the screen boundaries
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > screen_width- self.rect.width:
            self.rect.x = screen_width - self.rect.width

# Class for the falling balls
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load the ball image
        self.image = pygame.image.load("2574(1)(1).png")
        self.rect = self.image.get_rect()
        

        # Set the initial position and speed of the ball
        self.rect.x = random.choice(chicken_pos)+30
        self.rect.y = 150
        self.speedy = 4

    def update(self):
        # Move the ball downwards
        self.rect.y += self.speedy

        # Reset the position when the ball goes off the screen
        if self.rect.y > screen_height:
            self.rect.x = random.choice(chicken_pos)+30
            self.rect.y = 150
            self.speedy = 5
# Function to display the game over message
def game_over():
    messagebox.showinfo("Game Over", f"Your score: {score}")
    root.quit()
    pygame.quit()
# create the buttons objects
def draw_menu():
    command = -1
    pygame.draw.rect(screen, 'black', [100, 100, 300, 300])
    pygame.draw.rect(screen, 'green', [100, 100, 300, 300], 5)
    pygame.draw.rect(screen, 'white', [120, 120, 260, 40], 0, 5)
    pygame.draw.rect(screen, 'gray', [120, 120, 260, 40], 5, 5)
    txt = font.render('Menus Tutorial!', True, 'blue')
    screen.blit(txt, (135, 127))
    # menu exit button
    menu = Button('Exit Menu', (120, 350))
    menu.draw()
    button1 = Button('Options', (120, 180))
    button1.draw()
    button2 = Button('Settings', (120, 240))
    button2.draw()
    button3 = Button('Start Play', (120, 300))
    button3.draw()
    if menu.check_clicked():
        command = 0
    if button1.check_clicked():
        command = 1
    if button2.check_clicked():
        command = 2
    if button3.check_clicked():
        command = 3
    return command


def draw_game():
    menu_btn = Button('Main Menu', (230, 450))
    menu_btn.draw()
    menu = menu_btn.check_clicked()
    return menu
# Function to display the score
def display_score():
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, black)
    text_rect = text.get_rect()
    text_rect.center = (50, 50)
    screen.blit(text, text_rect)
#load the background
Farm=pygame.image.load("farm2.jpeg")
FarmBg=pygame.transform.scale(Farm, (800, 600))
Stick=pygame.image.load("Stick2.png")
Chicken_Stick=pygame.transform.scale(Stick, (800, 70))
#chicken cordinates
chicken_1 = 120
chicken_2 = 270
chicken_3 = 420
chicken_4 = 570
chicken_pos = [chicken_1,chicken_2, chicken_3,chicken_4]
#load the chickens images 
C=pygame.image.load("chicken.png")
Chicken=pygame.transform.scale(C, (90, 60))
#load the broken egg image 
broken_egg=pygame.image.load("broken_egg.png")
broken_eggs=pygame.transform.scale(broken_egg,(30,30))


# Create the basket object
basket = Basket()

# Create a group for the balls
balls = pygame.sprite.Group()


ball=Ball()
balls.add(ball) 



runing=True
clock=pygame.time.Clock()

while runing:
    screen.fill('light blue')
    clock.tick(60)
    if main_menu:
        menu_command = draw_menu()
        if menu_command != -1:
            main_menu = False
    else:
        main_menu = draw_game()
        if menu_command ==3:
            # Draw the basket, balls, and score label
            
            screen.blit(FarmBg, (0,0))
            screen.blit(Chicken_Stick,(0,120))
            for pos in chicken_pos:
                screen.blit(Chicken,(pos,100))
            screen.blit(basket.image, basket.rect)
            
            balls.draw(screen)
            balls.add(ball)
            balls.update()
            display_score()
        

        
    for event in pygame.event.get():
        if event.type==QUIT:
            runing=False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        basket.update('left')
    if keys[pygame.K_RIGHT]:
        basket.update('right')
    for ball in balls:
        if pygame.sprite.collide_rect(basket, ball):
            ball.kill()
            score+=1
            ball=Ball()
        # If all balls are caught, game over
        
        elif ball.rect.top >= screen_height:
            misses+=1
            balls.remove(ball)
            screen.blit(broken_eggs,(ball.rect.x,560))
            print(misses)
            if misses>=3:
              #stop the music for game 
              pygame.mixer.music.stop()
              game_over()
    
    
    
    
    
    

    
    pygame.display.update()
    
    
    
pygame.quit()
   
