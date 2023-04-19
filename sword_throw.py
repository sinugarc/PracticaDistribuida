#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 10:38:00 2023

@author: crishe07@ucm.es
"""

import pygame 

WIDTH=360
HEIGHT=480
FPS=60

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)

PLAYER1=0
PLAYER2=1

pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Sword throw")
clock=pygame.time.Clock()

font_name=pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
    font =pygame.font.Font(font_name,size)
    text_surface =font.render(text, True, WHITE)
    text_rect =text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface,text_rect)
    
    
#Def de clases


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((50,40))
        self.image.fill(GREEN)
        self.rect=self.image.get_rect()
        
        self.rect.x=5
        
        self.rect.y=HEIGHT/2 #en el lado
        self.angle=0 #esto todavia no sabemos cambiarlo
        self.speedy=0 # en principio la velocidad es constante
        
    def update(self): #de momento solo se mueve verticalmente 
        self.speedy=0    
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speedy=-2
        if keystate[pygame.K_DOWN]:
            self.speedy=2
        self.rect.y+=self.speedy
        #para que no se salga 
        if self.rect.top<0: 
            self.rect.y=0
        if self.rect.top>HEIGHT-45:
            self.rect.y=HEIGHT-45
            
    def throw(self):
        sword=Sword(self.rect.centerx, self.rect.centery, 0)
        all_sprites.add(sword)
        swords.add(sword)

class Sword(pygame.sprite.Sprite):
    def __init__(self,x,y,angle):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((10,10))
        self.image.fill(YELLOW)
        self.rect=self.image.get_rect()
        self.rect.centerx= x #empieza con la posicion del player
        self.rect.centery= y
        self.angle=angle
        self.speed= 10  #si somos el player 2, esto es negativo
        
        
    def update(self):
        self.rect.x+=self.speed
        
        #para que vaya en tal direccion
        #self.rect.y+=self.speed*self.angle
        
        #kill it if it moves off screen
        # if self.rect.top>0: #or self.rect.top>HEIGHT or self.rect.right>WIDTH or self.rect.left<0:
        #     self.kill()
            
    
class Target(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((20,20))
        self.image.fill(RED)
        self.rect=self.image.get_rect()
        
        self.rect.x=WIDTH-5
        
        self.rect.y=HEIGHT/2
        self.speedy=1
        
    def update(self):
        self.rect.y+=self.speedy
        #para que no se salga 
        if self.rect.top<0: 
            self.rect.y=0
            self.speedy*=-1
        if self.rect.top>HEIGHT-45:
            self.rect.y=HEIGHT-45
            self.speedy*=-1



#Generar sprites y grupos
all_sprites=pygame.sprite.Group()
swords=pygame.sprite.Group()



player=Player()
all_sprites.add(player)
target=Target()
all_sprites.add(target)


#Game loop
running=True
score=0
while running:
    clock.tick(FPS) #keep loop running at the right speed
    #Events
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_a:
                player.throw()
    
    #Update
    all_sprites.update()
    
    #un sword ha dado al target? si se chocan se elimina(True) 
    bullseye=pygame.sprite.spritecollide(target,swords,False)
    for b in bullseye:
        score+=1
    
    #Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen,str(score),18, WIDTH/2,10)
    pygame.display.flip() #se dibuja todo a la vez
    
pygame.quit()
print(score)