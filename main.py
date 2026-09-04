from pygame import *
import pygame
import time as tm
pygame.init()
mixer.init()
font.init()

win = display.set_mode((1600, 1000))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.player_image = transform.scale(image.load(player_image), (65, 65))
        self.rect = self.player_image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.player_speed = player_speed


    def resetSprite(self):
        win.blit(self.player_image, (self.rect.x, self.rect.y))

class Wall(sprite.Sprite):
    def __init__(self, wall_x, wall_y, wall_width, wall_height, color_1, color_2, color_3):
        super().__init__()
        self.cordinates = []
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
        self.i = 0
        self.old_time = tm.time()


    def draw_wall(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

    
    def rotate_wall(self):
        self.image = Surface((self.cordinates[self.i][2], self.cordinates[self.i][3]))
        self.rect = self.image.get_rect()
        self.rect.x = self.cordinates[self.i][0]
        self.rect.y = self.cordinates[self.i][1]


        win.blit(self.image, (self.cordinates[self.i][0], self.cordinates[self.i][1]))

        if (tm.time() - self.old_time) > 2:
            self.i += 1
            self.old_time = tm.time()
            
            if self.i == 3:
                self.i = 0

        







class Player(GameSprite):
    def update(self):
        key_press = key.get_pressed()

        if key_press[K_UP] and self.rect.y > 5:
            self.rect.y -= self.player_speed

        if key_press[K_DOWN] and self.rect.y < 950:
            self.rect.y += self.player_speed

        if key_press[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.player_speed
            
        if key_press[K_RIGHT] and self.rect.x < 1500:
            self.rect.x += self.player_speed

class Enemy(GameSprite):
    direction = "left"
    def update(self):
        
        if self.rect.x <= 1300:
                self.direction = "right"
        if self.rect.x >= 1600-85:
            self.direction = "left"
    
        if self.direction == "left":
            self.rect.x -= self.player_speed
        else:
            self.rect.x += self.player_speed

    direction2 = 'left'
    def update_for_difficultEnemy(self, moveX, moveY, moveX2, moveY2):
        if self.rect.x <= moveX and self.rect.y >= moveY:
                self.direction = "right"
        if self.rect.x >= moveX2 and self.rect.y <= moveY2:
            self.direction = "left"
    
        if self.direction == "left":
            self.rect.x -= self.player_speed
            self.rect.y += self.player_speed
        else:
            self.rect.x += self.player_speed
            self.rect.y -= self.player_speed

display.set_caption('Догонялки')
mixer.music.load('lessons/labirint_game/forgame.mp3')
lose_music = mixer.Sound('lessons/labirint_game/for_game.mp3')
fon = transform.scale(image.load('lessons/labirint_game/01.jpg'), (1600, 1000))
mixer.music.play(0)

x1 = 100
y1 = 500
player = Player('lessons/labirint_game/pacman_PNG82.png', 65, 65, 10)
en1 = Enemy('lessons/labirint_game/enemy.png', 1300, 500, 5)
en2 = Enemy('lessons/labirint_game/enemy.png', 525, 1000-85, 3)
finaly = GameSprite('lessons/labirint_game/finaly.png', 1500, 50, 0)
game_key = GameSprite('lessons/labirint_game/key.png', 800, 50,  0)
w1 = Wall(250, 0, 25, 800, 0, 255, 0)
w2 = Wall(500, 200, 25, 800, 0, 255, 0 )
w3 = Wall(750, 0, 25, 800, 0, 255, 00)
w4 = Wall(1000, 200, 25, 800, 0, 255, 0)
w5 = Wall(1250, 0, 25, 800, 0, 255, 0)
w6 = Wall(500, 0, 25, 225, 0, 225, 0)
door = Wall(1250, 800, 25, 200, 40, 40, 40)

w6.cordinates = [[w6.rect.x, w6.rect.y, w6.width, w6.height], [525, 200, 225, 25], [275, 200, 225, 25]]
clock = time.Clock()
font = font.Font(None, 90)
text_win = font.render('YOU WIN!', True, (201, 255, 0))
text_lose = font.render('YOU LOSE!', True, (225, 0, 0))
game = True
finish = False
key_is_taking = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        win.blit(fon, (0, 0))
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.rotate_wall()
        door.draw_wall()
        player.resetSprite()
        en1.resetSprite()
        en2.resetSprite()
        finaly.resetSprite()
        if key_is_taking == False:
            game_key.resetSprite()
        player.update()
        en1.update()
        en2.update_for_difficultEnemy(525, 1000-85, 700, 900)

        if sprite.collide_rect(player, finaly):
            finish = True
            win.blit(text_win, (600, 500))

        elif sprite.collide_rect(player, en1):
            finish = True
            win.blit(text_lose, (600, 500))
            lose_music.play()
            

        elif sprite.collide_rect(player, en2):
            finish = True
            win.blit(text_lose, (600, 500))
            lose_music.play()
        
        elif sprite.collide_rect(player, w1):
            finish = True
            win.blit(text_lose, (600, 500))
            lose_music.play()

        elif sprite.collide_rect(player, w2):
            finish = True
            win.blit(text_lose, (600, 500))
            lose_music.play()

        elif sprite.collide_rect(player, w3):
            finish = True
            win.blit(text_lose, (600, 500))
            lose_music.play()

        elif sprite.collide_rect(player, w4):
            finish = True
            win.blit(text_lose, (600, 500))
            lose_music.play()

        elif sprite.collide_rect(player, w5):
            finish = True
            win.blit(text_lose, (600, 500))
            lose_music.play()

        elif sprite.collide_rect(player, w6):
            finish = True
            win.blit(text_lose, (600, 500))
            lose_music.play()

        elif sprite.collide_rect(player, game_key) and key_is_taking == False:
            key_is_taking = True

        
        elif sprite.collide_rect(player, door) and key_is_taking == True:
            door.image = Surface((200, 25))
            door.image.fill((40, 40, 40))
            door.rect = door.image.get_rect()
            door.rect.x = 1025
            door.rect.y = 800
            win.blit(door.image, (door.rect.x, door.rect.y))

        elif sprite.collide_rect(player, door) and key_is_taking == False:
            player.rect.x -= 12





        

    
    


    display.update()
    clock.tick(60)