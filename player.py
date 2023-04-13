from multiprocessing.connection import Client
import traceback
import pygame
import sys, os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
GREEN = (0,255,0)
X = 0
Y = 1
SIZE = (700, 525)

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

class Sword():
    def __init__(self, side):
        self.side = side
        self.pos = [None, None]
        self.angle= 0
        
    def get_pos(self):
        return self.pos

    def get_side(self):
        return self.side

    def set_pos(self, pos):
        self.pos = pos

    def set_angle(self, angle):
        self.angle=angle
        
    def __str__(self):
        return f"P<{SIDES[self.side], self.pos}>"

class Target():
    def __init__(self,side):
        self.side=side
        self.pos=[ None, None ]

    def get_pos(self):
        return self.pos
    
    def get_side(self):
        return self.side


    def set_pos(self, pos):
        self.pos = pos

    def __str__(self):
        return f"B<{self.pos}>"


class Game():
    def __init__(self):
        self.swords = [Sword(i) for i in range(2)]
        self.targets = [Target(i) for i in range(2)]
        self.score = [0,0]
        self.running = True

    def get_sword(self, side):
        return self.swords[side]

    def set_pos_sword(self, side, pos):
        self.swords[side].set_pos(pos)


    def get_target(self,side):
        return self.targets[side]

    def set_targets_pos(self, side, pos):
        self.targets[side].set_pos(pos)

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score


    def update(self, gameinfo):
        self.set_pos_player(LEFT_PLAYER, gameinfo['pos_left_player'])
        self.set_pos_player(RIGHT_PLAYER, gameinfo['pos_right_player'])
        self.set_ball_pos(LEFT_PLAYER, gameinfo['pos_left_ball'])
        self.set_ball_pos(RIGHT_PLAYER, gameinfo['pos_left_ball'])
        self.set_score(gameinfo['score'])
        self.running = gameinfo['is_running']

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False

    def __str__(self):
        return f"G<{self.players[RIGHT_PLAYER]}:{self.players[LEFT_PLAYER]}:{self.ball}>"


class TargetSprite(pygame.sprite.Sprite):
    def __init__(self, player):
      super().__init__()
      self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
      self.image.fill(BLACK)
      self.image.set_colorkey(BLACK)#drawing the paddle
      self.player = player
      color = PLAYER_COLOR[self.player.get_side()]
      pygame.draw.rect(self.image, color, [0,0,PLAYER_WIDTH, PLAYER_HEIGHT])
      self.rect = self.image.get_rect()
      self.update()

    def update(self):
        pos = self.player.get_pos()
        self.rect.centerx, self.rect.centery = pos

    def __str__(self):
        return f"S<{self.player}>"


class SwordSprite(pygame.sprite.Sprite):
    def __init__(self, ball):
        super().__init__()
        self.ball = ball
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, BALL_COLOR, [0, 0, BALL_SIZE, BALL_SIZE])
        self.rect = self.image.get_rect()
        self.update()

    def update(self):
        pos = self.ball.get_pos()
        self.rect.centerx, self.rect.centery = pos



class Display():
    def __init__(self, game):
        self.game = game
        self.paddles = [Paddle(self.game.get_player(i)) for i in range(2)]

        self.ball = BallSprite(self.game.get_ball())
        self.all_sprites = pygame.sprite.Group()
        self.paddle_group = pygame.sprite.Group()
        for paddle  in self.paddles:
            self.all_sprites.add(paddle)
            self.paddle_group.add(paddle)
        self.all_sprites.add(self.ball)

        self.screen = pygame.display.set_mode(SIZE)
        self.clock =  pygame.time.Clock()  #FPS
        self.background = pygame.image.load('background.png')
        pygame.init()

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
            elif event.type == pygame.QUIT:
                events.append("quit")
        if pygame.sprite.collide_rect(self.ball, self.paddles[side]):
            events.append("collide")
        return events


    def refresh(self):
        self.all_sprites.update()
        self.screen.blit(self.background, (0, 0))
        score = self.game.get_score()
        font = pygame.font.Font(None, 74)
        text = font.render(f"{score[LEFT_PLAYER]}", 1, WHITE)
        self.screen.blit(text, (250, 10))
        text = font.render(f"{score[RIGHT_PLAYER]}", 1, WHITE)
        self.screen.blit(text, (SIZE[X]-250, 10))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def tick(self):
        self.clock.tick(FPS)

    @staticmethod
    def quit():
        pygame.quit()


def main(ip_address):
    try:
        with Client((ip_address, 6000), authkey=b'secret password') as conn:
            game = Game()
            side,gameinfo = conn.recv()
            print(f"I am playing {SIDESSTR[side]}")
            game.update(gameinfo)
            display = Display(game)
            while game.is_running():
                events = display.analyze_events(side)
                for ev in events:
                    conn.send(ev)
                    if ev == 'quit':
                        game.stop()
                conn.send("next")
                gameinfo = conn.recv()
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
    main(ip_address)
