from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Rocket(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):
        bullet = KillBullet('bullet.png', self.rect.centerx, self.rect.y, 5, 15, 20)
        bullets.add(bullet)

lost = 0
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(0, win_width - 80)
            lost += 1

class EnemyBoss(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(0, win_width - 80)
            lost += 10

prop = 0
class KillBullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

asteroids = sprite.Group()
for i in range(2):
    asteroid = Enemy('asteroid.png', randint(0, 700 - 80), 0, randint(1,3), 80, 50)
    asteroids.add(asteroid)



rocket = Rocket('rocket.png', 10, 400, 7, 80, 100)
bullets = sprite.Group()

enemys = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(0, 700 - 80), 0, randint(1,3), 80, 50)
    enemys.add(enemy)

enemyBoss = EnemyBoss('ufo.png', randint(0, 700 - 80), 0, randint(1,3), 200, 200)
win_width = 700
win_height = 500
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)

window = display.set_mode((win_width, win_height))
display.set_caption('spacegame')
Clock = time.Clock()
FPS = 90

font.init()
Lable = font.SysFont('Arial', 30)
Lable1 = font.SysFont('Arial', 120)
finish = False

background = transform.scale (image.load('galaxy.jpg'),(700,500))

rel_time = False
num_fire = 0

gameshuter = True
while gameshuter:
    for i in event.get():
        if i.type == QUIT:
            gameshuter = False
        if i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fire<10:
                    rocket.fire()
                    num_fire += 1
                else:
                    rel_time = True
                    Start_timer = timer()
                

                


    
    if finish != True:
        window.blit(background, (0,0))
        text_prop = Lable.render('Пропусков:'+str(lost), 1, (255, 255, 255))
        text_score = Lable.render('Счет:'+str(prop), 1 ,(255, 255, 255))
        text_prop1 = Lable1.render('lose', 1, (255, 0, 0))
        text_score1 = Lable1.render('win', 1 ,(255, 255, 255))


        rocket.reset()
        window.blit(text_score ,(5, 10))
        window.blit(text_prop, (5, 50))
        rocket.update()
        bullets.update()
        enemys.update()
        bullets.draw(window)
        asteroids.draw(window)
        asteroids.update()
        enemys.draw(window)
        now_time = timer()
        if rel_time == True and now_time - Start_timer < 1:
            reload_text = Lable.render('WAIT,RELOAD   ' + str(round(now_time - Start_timer,2)) ,True ,(255, 0, 0))
            window.blit(reload_text, (250, 450))
        elif rel_time == True and now_time - Start_timer > 1:
            rel_time = False
            num_fire = 0
        if sprite.groupcollide(enemys, bullets, True, True):
            enemy = Enemy('ufo.png', randint(0, 700 - 80), 0, randint(1,3), 80, 50)
            enemys.add(enemy)
            prop +=1
        if sprite.groupcollide(enemys, bullets, True, True):
            enemy = Enemy('ufo.png', randint(0, 700 - 80), 0, randint(1,3), 80, 50)
            enemys.add(enemy)
            prop += 1
        if lost > 10 or sprite.spritecollide(rocket, asteroids,False):
            window.blit(text_prop1, (250, 200))
            finish = True
        if prop > 11:
            finish = True
            window.blit(text_score1, (260, 200))
    else:
        finish = False
        time.delay(2000)
        lost = 0
        prop = 0
        for i in asteroids:
            i.kill()
        for i in enemys:
            i.kill()
        for i in bullets:
            i.kill()
        for i in range(2):
            asteroid = Enemy('asteroid.png', randint(0, 700 - 80), 0, randint(1,3), 80, 50)
            asteroids.add(asteroid)
        for i in range(5):
            enemy = Enemy('ufo.png', randint(0, 700 - 80), 0, randint(1,3), 80, 50)
            enemys.add(enemy)

        
    display.update()
    Clock.tick(FPS)