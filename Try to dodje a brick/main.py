from pygame import *
from random import randint
import time
from pygame.time import delay

#Основ. окно игры
win_width = 1000 #ширина
win_height = 800 #высота
window = display.set_mode((win_width, win_height))
display.set_caption('Try to dodge a brick')
background = transform.scale(image.load('background.png'), (win_width, win_height))

#Константы
run = True
finish = False
#clock = time.Clock()
life = 3
score = 1

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y,):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (100, 120))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Класс игрока
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 1:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 900:
            self.rect.x += self.speed

#Класс кирпича(врага)
class Brick(GameSprite):
    def update(self):
        self.rect.y += self.speed
        #Исчезновение при прикосновение границы экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

#Сам игрок
player = Player('player.png', 500, 680, 7, 80, 120)

#Кирпичи летят
bricks = sprite.Group()
for i in range(1, 4):
    brick = Brick('brick.png', randint(-5, win_width - 95), -140, randint(3, 5), 50, -40)
    bricks.add(brick)

#Текст
font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
lose = font1.render('Nice try!', True, (180, 0, 0))
win = font1.render('GG!', True, (0, 180, 0))

#Музыка и звуки
mixer.init()
mixer.music.load('background_music.mp3')
hit_sound = mixer.Sound('hit.ogg')
lose_sound = mixer.Sound('lose_sound.ogg')
win_sound = mixer.Sound('win_sound.wav')

#Цикл игры
mixer.music.play() #это для запуска музыки
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    if not finish:
        window.blit(background,(0,0))

        #Очки
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        #Увеличение очков
        score += 1

        #Поражение
        if life == 0:
            finish = True
            window.blit(lose, (400, 370))
            mixer.music.stop()
            lose_sound.play()

        #Выигрыш
        if score >= 3001:
            finish = True
            window.blit(win, (450, 370))
            mixer.music.stop()
            win_sound.play()

        #Изменение цвета жизней
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
    
        #Показ жизней на экране
        text_life = font2.render('Кол-во жизей:' + str(life), 1, life_color)
        window.blit(text_life, (10, 45))

        #Уменьшение жизни при столкновении с кирпичом
        if sprite.spritecollide(player, bricks, False):
            sprite.spritecollide(player, bricks, True)
            hit_sound.play()
            life = life -1
            for i in range(1, 2):
                brick = Brick('brick.png', randint(-5, win_width - 95), -140, randint(3, 5), 50, -40)
                bricks.add(brick)

        #Обновление игрока и кирпича
        player.update()
        player.reset()
        bricks.update()
        bricks.draw(window)
        
        display.update()

    #Автомат. перезагрузка
    else:
        finish = False
        score = 0
        life = 3
        for m in bricks:
            m.kill()
              
        for i in range(1, 4):
            brick = Brick('brick.png', randint(-5, win_width - 95), -140, randint(3, 5), 50, -40)
            bricks.add(brick)
            
        delay(3000)
        mixer.music.play()