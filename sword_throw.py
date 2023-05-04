import pygame 
from os import path

WIDTH=1060
HEIGHT=600
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
img_dir = path.join(path.dirname(__file__), 'img')
player_img = pygame.image.load(path.join(img_dir, "sword.png")).convert_alpha()
laser_img = pygame.image.load(path.join(img_dir,"laser1.png")).convert_alpha()
target_img = pygame.image.load(path.join(img_dir, "target2.png")).convert_alpha()
 
#Generar sprites y grupos
all_sprites=pygame.sprite.Group()
swords=pygame.sprite.Group()
    
    
    
    

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

        self.player_img_peq=pygame.transform.smoothscale(player_img,(60,90))
        self.image=self.player_img_peq
        
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        
        self.rect.x=50
        
        self.rect.y=HEIGHT/2 #en el lado
        self.rot=0 
        self.rot_speed=0
        self.speedy=0 # en principio la velocidad es constante
        
    def update(self): #de momento solo se mueve verticalmente 
        self.speedy=0    
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speedy=-2
        if keystate[pygame.K_DOWN]:
            self.speedy=2
        if keystate[pygame.K_LEFT]:
            self.rot_speed=2
        if keystate[pygame.K_RIGHT]:
            self.rot_speed=-2
        self.rect.y+=self.speedy
        #para que no se salga 
        if self.rect.top<0: 
            self.rect.y=0
        if self.rect.top>HEIGHT-45:
            self.rect.y=HEIGHT-45
       
            
            
        self.rot=(self.rot +self.rot_speed)
        self.rot_speed=0
        if self.rot>90:
            self.rot=90
        if self.rot < -90:
            self.rot=-90
        self.image=pygame.transform.rotate(self.player_img_peq,self.rot)

            
    def throw(self):
        sword=Sword(self.rect.centerx, self.rect.centery, self.rot)
        all_sprites.add(sword)
        swords.add(sword)

class Sword(pygame.sprite.Sprite):
    def __init__(self,x,y,angle):
        pygame.sprite.Sprite.__init__(self)
        
        self.image=laser_img
        self.image=pygame.transform.smoothscale(self.image,(40,10))
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.centerx= x #empieza con la posicion del player
        self.rect.centery= y
        self.angle=angle
        self.speed= 10  #si somos el player 2, esto es negativo
        
        
    def update(self):
        self.rect.centerx+=self.speed
        self.rect.centery+=self.speed*self.angle/-100
      
        
        #kill it if it moves off screen
        if self.rect.top>HEIGHT or self.rect.right>WIDTH: 
            self.kill()
            
    
class Target(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image=target_img
        self.image=pygame.transform.smoothscale(self.image,(20,80))
 
        self.rect=self.image.get_rect()
        
        self.rect.x=WIDTH-10
        
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


def main():

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
                if event.key==pygame.K_SPACE:
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
    
if __name__=='__main__':
    main()