from pygame import *
font.init()
'''Необходимые классы'''

#класс-родитель для спрайтов 
class GameSprite(sprite.Sprite):    #конструктор класса
    def __init__(self, in_image, in_size_x, in_size_y, in_coord_x, in_coord_y):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(in_image), (in_size_x, in_size_y))
        self.rect = self.image.get_rect()
        self.rect.x = in_coord_x
        self.rect.y = in_coord_y
        self.size_x = in_size_x
        self.size_y = in_size_y
    def blit(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class MoveSprite(GameSprite):    #конструктор класса
    def __init__(self, in_image, in_size_x, in_size_y, in_coord_x, in_coord_y, in_speed):
        super().__init__(in_image, in_size_x, in_size_y, in_coord_x, in_coord_y)
        self.speed = in_speed
    def move(self,x,y):
        self.rect.x += self.speed*x
        self.rect.y += self.speed*y

class PlayerSprite(MoveSprite):
    def move(self):       
       keys = key.get_pressed()
       if keys[K_a] and self.rect.x > self.speed:
           super().move(-1,0)
       if keys[K_d] and self.rect.x < win_width - self.size_x:
           super().move(1,0)
       if keys[K_w] and self.rect.y > self.speed:
           super().move(0,-1)
       if keys[K_s] and self.rect.y < win_height - self.size_y:
           super().move(0,1)
    def remove(self):       
       keys = key.get_pressed()
       if keys[K_a] and self.rect.x > self.speed:
           super().move(1,0)
       if keys[K_d] and self.rect.x < win_width - self.size_x:
           super().move(-1,0)
       if keys[K_w] and self.rect.y > self.speed:
           super().move(0,1)
       if keys[K_s] and self.rect.y < win_height - self.size_y:
           super().move(0,-1)

class EnemySprite(MoveSprite):
   direction = 1
   def move(self):
       if self.rect.x <= 470:
           self.direction = 1
       if self.rect.x >= win_width - 85:
           self.direction = -1
       super().move(self.direction,0)

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



#Игровая сцена:
win_width = 700
win_height = 500
sprite_size = 50
window = display.set_mode((win_width, win_height))
display.set_caption("Догонялки")
background = GameSprite('background.jpg', win_width,win_height,0,0)

#Персонажи игры:
player = PlayerSprite('hero.png', sprite_size,sprite_size,20,30,5)
cyborg = EnemySprite('cyborg.png', sprite_size,sprite_size,win_width - 220,win_height - 180,5)
final =  GameSprite('treasure.png', sprite_size,sprite_size,win_width - 120, win_height - 80)

wall = Wall(255, 255, 255, 80, 400, 10, 300)
wall2 = Wall(255, 255, 255, 80, 0, 10, 300)
wall3 = Wall(255, 255, 255, 440, 100, 10, 400)
wall4 = Wall(255, 255, 255, 440, 100, 150, 10)
wall5 = Wall(255, 255, 255, 290, 100, 150, 10)

finish = False
game = True
clock = time.Clock()
FPS = 60

font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (255, 0, 0))
#музыка
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        background.blit()
        player.blit()
        cyborg.blit()
        final.blit()
        wall.draw_wall()
        wall2.draw_wall()
        wall3.draw_wall()
        wall4.draw_wall()
        wall5.draw_wall()
        if sprite.collide_rect(player, final):
            window.blit(win, (200, 200))
            finish = True
        if sprite.collide_rect(player, cyborg):
            window.blit(lose, (200, 200))
            finish = True
        if sprite.collide_rect(player, wall):
            player.remove()

    


    player.move()
    cyborg.move()

    display.update()
    clock.tick(FPS)