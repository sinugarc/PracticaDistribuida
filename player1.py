from multiprocessing.connection import Client
import traceback
import pygame
import sys, os

from os import path
# pygame.init()
img_dir = path.join(path.dirname(__file__), 'img')
# player_img = pygame.image.load(path.join(img_dir, "sword.png")).convert_alpha()
# target_img = pygame.image.load(path.join(img_dir, "target2.png")).convert_alpha()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
GREEN = (0,255,0)
X = 0
Y = 1
SIZE = (900, 605)

LEFT_PLAYER = 0
RIGHT_PLAYER = 1
PLAYER_COLOR = [GREEN, YELLOW]
PLAYER_HEIGHT = 60
PLAYER_WIDTH = 10

BALL_COLOR = WHITE
BALL_SIZE = 10
FPS = 60


SIDES = ["left", "right"]
SIDESSTR = ["left", "right"]

class Player():
    def __init__(self, side):
        self.side = side
        self.pos = [None, None]
        self.angle= 0


class Sword():
    def __init__(self, side, pos, velocity,angle):
        self.side=side
        self.pos=pos 
        self.velocity=velocity
        self.angle=angle
        


class Game():
    def __init__(self):
        self.players = [Player(i) for i in range(2)]
        self.swords= [Sword(i,self.players[i].pos, 0, self.players[i].angle) for i in range(2)]
        #self.targets= [Target(i) for i in range(2)]
        self.score = [0,0]
        self.running = True

    def set_pos_player(self, side, pos): 
        self.players[side].pos=pos
    
    def set_pos_sword(self, side, pos):
        self.swords[side].pos=pos
        
    def set_score(self, score):
        self.score = score

    def update(self, gameinfo):
        self.set_pos_player(LEFT_PLAYER, gameinfo['pos_left_player'])
        self.set_pos_player(RIGHT_PLAYER, gameinfo['pos_right_player'])
        self.set_pos_sword(LEFT_PLAYER, gameinfo['pos_left_sword'])
        self.set_pos_sword(RIGHT_PLAYER, gameinfo['pos_right_sword'])
        #self.set_pos_target(LEFT_PLAYER, gameinfo['pos_left_target'])
        #self.set_pos_target(RIGHT_PLAYER, gameinfo['pos_right_target'])
        self.set_score(gameinfo['score'])
        self.running = gameinfo['is_running']

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False

    # def __str__(self):
    #     return f"G<{self.players[RIGHT_PLAYER]}:{self.players[LEFT_PLAYER]}:{self.ball}>"


   
class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self,player):
         pygame.sprite.Sprite.__init__(self)
         #self.image=pygame.Surface((50,40))
         player_img = pygame.image.load("sword.png")
         self.player_img_peq=pygame.transform.smoothscale(player_img,(70,40))
         self.image=self.player_img_peq
         self.image.set_colorkey(GREEN)
         self.rect=self.image.get_rect()
         
         self.player=player
         self.update()
         
    def update(self):
         pos=self.player.pos#get_pos()
         angle=self.player.angle#get_angle()
         self.rect.centerx,self.rect.centery=pos
         self.image=pygame.transform.rotate(self.player_img_peq,angle)
         
        
class SwordSprite(pygame.sprite.Sprite):
    def __init__(self,sw):
         pygame.sprite.Sprite.__init__(self)
         #self.image=pygame.Surface((50,40))
         player_img = pygame.image.load("sword.png")
         self.player_img_peq=pygame.transform.smoothscale(player_img,(10,40))
         self.image=self.player_img_peq
         self.image.set_colorkey(GREEN)
         self.rect=self.image.get_rect()
         
         self.sw=sw
         self.update()
         
    def update(self):
         pos=self.sw.pos
         angle=self.sw.angle
         self.rect.centerx,self.rect.centery=pos
         self.image=pygame.transform.rotate(self.player_img_peq,angle)


class TargetSprite(pygame.sprite.Sprite):
    def __init__(self,side):
        pygame.sprite.Sprite.__init__(self)
        #self.image=pygame.Surface((20,20))
        #self.image.fill(RED)
        #self.image.set_colorkey(BLUE)
        target_img = pygame.image.load("target2.png")
        self.image=target_img
        self.image=pygame.transform.smoothscale(self.image,(20,80))
 
        self.rect=self.image.get_rect()
        self.speed=2
        if side==0:
            self.rect.x=SIZE[X]-10
        else:
            self.rect.x=10
        self.rect.y= SIZE[Y]//2
        self.update()
        
    def update(self):
        # pos=self.target.get_pos()
        # self.rect.centerx,self.rect.centery=pos
        self.rect.y+=self.speed
        #para que no se salga 
        if self.rect.top<0: 
            self.rect.y=0
            self.speed*=-1
        if self.rect.top>SIZE[Y]-45:
            self.rect.y=SIZE[Y]-45
            self.speed*=-1

class Display():
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.targets = [TargetSprite(i) for i in range(2)]
        self.players= [PlayerSprite(self.game.players[i]) for i in range(2)]
        self.sword=[SwordSprite(self.game.swords[i]) for i in range(2)]
       
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.targets[0])
        self.all_sprites.add(self.targets[1])
        self.all_sprites.add(self.players[0])
        self.all_sprites.add(self.players[1])

        self.screen = pygame.display.set_mode(SIZE)
        self.clock =  pygame.time.Clock()  #FPS
        
        #self.background = pygame.image.load('background.png')
        # self.player_img = pygame.image.load(path.join(img_dir, "sword.png")).convert_alpha()
        # self.target_img = pygame.image.load(path.join(img_dir, "target2.png")).convert_alpha()

        pygame.init()
        pygame.display.set_caption("Sword throw 1" )

    def analyze_events(self, side):
        events = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    events.append("quit")
                elif event.key == pygame.K_UP:
                    events.append("up")
                elif event.key == pygame.K_DOWN:
                    events.append("down")
                elif event.key == pygame.K_LEFT:
                    events.append("left")
                elif event.key == pygame.K_RIGHT:
                    events.append("right")
                elif event.key == pygame.K_SPACE:
                    events.append("space")
                                  
            elif event.type == pygame.QUIT:
                events.append("quit")
        if pygame.sprite.collide_rect(self.sword[side], self.targets[(side+1)%2]):
             events.append("collide")
        return events


    def refresh(self):
        self.all_sprites.update()
        #self.screen.blit(self.background, (0, 0))
        score = self.game.score#get_score()
        font = pygame.font.Font(None, 74)
        text = font.render(f"{score[LEFT_PLAYER]}", 1, WHITE)
        self.screen.blit(text, (250, 10))
        text = font.render(f"{score[RIGHT_PLAYER]}", 1, WHITE)
        self.screen.blit(text, (SIZE[X]-250, 10))
        #self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def tick(self):
        self.clock.tick(FPS)

    @staticmethod
    def quit():
        pygame.quit()


def main(ip_address,side):
    try:
        with Client((ip_address, 6000), authkey=b'secret password') as conn:
            game = Game()
            side,gameinfo = conn.recv()
            print(f"I am playing {side}")
            game.update(gameinfo)
            display = Display(game)
            while game.is_running():
                events = display.analyze_events(side)
                for ev in events:
                    conn.send(ev)
                    if ev == 'quit':
                        game.stop()
                conn.send("next")
                side, gameinfo = conn.recv()
                game.update(gameinfo)
                display.refresh()
                display.tick()
    except:
        traceback.print_exc()
    finally:
        pygame.quit()


if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
        #side=sys.argv[1]
    main(ip_address,1)