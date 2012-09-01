#       VERSION .2  (062412)#
#  new in this version:     #
#   - Added animation funcs #
#   -                       #
#   -                       #
#############################
import pygame
import time
import random
class Sprite(pygame.sprite.Sprite):
    def __init__(self, filename, XPOS=0, YPOS=0, FILL=(255,255,255)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/' + filename).convert()
        self.image.set_colorkey(-1)
        #self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.rect.x = XPOS
        self.rect.y = YPOS
        self.moving = {'down':0,'up':0,'left':0,'right':0}
        self.old = (0,0,0,0)
        self.blank = pygame.Surface((self.rect.width,self.rect.height))
        self.blank.fill(FILL)
        self.firing = 0
        self.time = 0
        self.timer = 0
    def Move(self,SPEED=5):
        self.old = self.rect
        if self.moving['down'] == 1:
            self.rect.y += SPEED
        if self.moving['up'] == 1:
            self.rect.y -= SPEED
        if self.moving['left'] == 1:
            self.rect.x -= SPEED
        if self.moving['right'] == 1:
            self.rect.x += SPEED
    def SetUpAnimation(self,FRAMES):
        self.frames = FRAMES
        self.numOfFrames = len(FRAMES)
        self.curFrame = 0
        framelist = []
        for image in self.frames:
            framelist.append(pygame.image.load('data/' + image).convert())
        self.frames = tuple(framelist)
    def Animate(self):
        #increment the frame number/ show the next image in the animation sequence
        self.curFrame += 1
        #if there are no more frames, go back to frame 1
        if self.curFrame > (self.numOfFrames - 1):
            self.curFrame = 0
        #set the sprites image to the current frame
        self.image = self.frames[self.curFrame]
    def Fire(self,group,bullet):
        if self.firing == 1:
            self.time = round(time.time(), 2)
            if self.timer == 0:
                self.timer = self.time + 0.05
            if self.time >= self.timer:
                group.add(bullet)
                self.timer = 0
    def Blank(self,screen):
        screen.blit(self.blank,self.old)
    def Draw(self,screen):
        screen.blit(self.image,self.rect)
class Bullet(pygame.sprite.Sprite):
    def __init__(self,player,speed,filename='bullet.png'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/' + filename).convert()
        self.image.set_colorkey((255,255,255))
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x+(player.rect.width/2)
        self.rect.y = player.rect.y+(player.rect.height/2)-(self.rect.height/2)
        self.moving = {'down':0,'up':0,'left':0,'right':0}
        self.old = (0,0,0,0)
        self.blank = pygame.Surface((self.rect.width,self.rect.height))
        self.blank.fill((255,255,255))
        self.speed = speed
    def Move(self):
        self.old = self.rect
        self.rect = self.rect.move([self.speed,0])
        if self.rect.x >= (pygame.display.get_surface().get_rect().width+1):
            self.kill()
    def Draw(self,screen):
        screen.blit(self.blank,self.old)
        screen.blit(self.image,self.rect)
    def Erase(self,screen):
        screen.blit(self.blank,self.rect)
class Enemy(pygame.sprite.Sprite):
    def __init__(self,screen,speed=-3,filename='enemy.png'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/' + filename).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_rect().width-10
        self.rect.y = random.randint(0,screen.get_rect().height)
        self.moving = {'down':0,'up':0,'left':0,'right':0}
        self.old = (0,0,0,0)
        self.blank = pygame.Surface((self.rect.width,self.rect.height))
        self.blank.fill((255,255,255))
        self.speed = speed
        self.health = 100
    def Move(self):
        self.old = self.rect
        self.rect = self.rect.move([self.speed,0])
        if self.rect.x <= 0-self.rect.width:
            self.kill()
    def Draw(self,screen):
        screen.blit(self.blank,self.old)
        screen.blit(self.image,self.rect)
    def Erase(self,screen):
        screen.blit(self.blank,self.rect)
    def HealthCheck(self):
        if self.health <= 0:
            return True        
