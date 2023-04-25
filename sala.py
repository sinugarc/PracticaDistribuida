from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Value, Lock
import traceback
import sys
import pygame

LEFT_PLAYER = 0
RIGHT_PLAYER = 1
SIDESSTR = ["left", "right"]
SIZE = (900, 605)
X=0
Y=1
DELTA = 30
DELTA_2 = 2


class Player():
    def __init__(self, side):
        self.side = side
        if side == LEFT_PLAYER:
            self.pos = [5, SIZE[Y]//2]
        else:
            self.pos = [SIZE[X] - 5, SIZE[Y]//2]
        self.angle = 0


    def moveDown(self):
        self.pos[Y] += DELTA
        if self.pos[Y] > SIZE[Y]:
            self.pos[Y] = SIZE[Y]

    def moveUp(self):
        self.pos[Y] -= DELTA
        if self.pos[Y] < 0:
            self.pos[Y] = 0
            
    def AngleUp(self):
        self.angle += DELTA_2
        if self.angle > 90:
            self.angle = 90
    
    def AngleDown(self):
        self.angle -= DELTA_2
        if self.angle < -90:
            self.angle = -90
    
    def throw(self,sword):
        #Le pasamos una velocidad 10
        sw=sword  #= Sword(self.pos,10, self.angle)
        sw.pos=self.pos
        sw.angle=self.angle
        sw.velocity=10
        return sw
    
    def __str__(self):
        return f"P<{SIDESSTR[self.side]}, {self.pos}>"


class Sword():
    #Podemos o bien pasar side para saber si usamos velocidad positiva
    #o negativa o pasar directamente una velocida entera 
    def __init__(self, side,playerpos,velocity,angle):
        
        self.side=side
        self.pos=playerpos #Sera una tupla o lista de dos elementos
        self.velocity=velocity
        self.angle=angle
        
    
    def update(self):
        self.pos[X] += self.velocity[X]
        self.pos[Y] += self.velocity[Y]*self.angle/-100
        
    
    #Tb hay que pensar si añadir un collide_swords
    
    # def __str__(self):
    #     return f"B<{self.pos, self.velocity,self.angle}>"
    

class Game():
    def __init__(self, manager):
        self.players = manager.list( [Player(LEFT_PLAYER), Player(RIGHT_PLAYER)] )
        p0=self.players[0]
        p1=self.players[1]
        self.swords = manager.list( [Sword(0,p0.pos,0,p0.angle), Sword(1,p1.pos,0,p1.angle)] )
        #se deberian iniciar estas Sword con velocidad 0
        
        self.score = manager.list( [0,0] )
        self.running = Value('i', 1) # 1 running
        self.lock = Lock()

    # def get_player(self, side):
    #     return self.players[side]

    # def get_swords(self,side):
    #     return self.swords[side]
    
    # def get_targets(self,side):
    #     return self.targets[side]

    # def get_score(self):
    #     return list(self.score)

    def is_running(self):
        return self.running.value == 1

    def stop(self):
        self.running.value = 0

    def moveUp(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.moveUp()
        self.players[player] = p
        self.lock.release()

    def moveDown(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.moveDown()
        self.players[player] = p
        self.lock.release()
    
    def AngleUp(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.AngleUp()
        self.players[player] = p
        self.lock.release()
        
    def AngleDown(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.AngleDown()
        self.players[player] = p
        self.lock.release()
    
    
    def throw(self,player):
        self.lock.acquire()
        p = self.players[player]
        sw=self.swords[player]
        sword=p.throw(sw)
        self.swords[player]=sword
        self.lock.release()
   
    
    #colisiones y cambio score
    def collide(self,sword):
        #sword vuelve a la posicion original de player
        self.lock.acquire()
        pos1=self.players[player].pos
        angle1=self.players[player].angle
        sw=self.swords[player]
        sw.pos=pos1 
        sw.angle=angle1
        sw.velocity=0
        self.lock.release()
        
    def get_info(self):
        info = {
            'pos_left_player': self.players[LEFT_PLAYER].pos,
            'pos_right_player': self.players[RIGHT_PLAYER].pos,
            'pos_left_sword': self.swords[LEFT_PLAYER].pos,
            'pos_right_sword': self.swords[RIGHT_PLAYER].pos,
            #'pos_left_target': self.targets[LEFT_PLAYER].get_pos(),
            #'pos_right_target': self.targets[RIGHT_PLAYER].get_pos(),
            'score': list(self.score),
            'is_running': self.running.value == 1
        }
        return info
   

    # def __str__(self):
    #     return f"G<{self.players[RIGHT_PLAYER]}:{self.players[LEFT_PLAYER]}:{self.ball[0]}:{self.running.value}>"


""""""""""""""""""""""""""""""""""""""""""""""""""""""


def player(side, conn, game):
    try:
        print(f"starting player {SIDESSTR[side]}:{game.get_info()}")
        conn.send( (side, game.get_info()) )
        while game.is_running():
            command = ""
            while command != "next":
                command = conn.recv()
                if command == "up":
                    game.moveUp(side)
                elif command == "down":
                    game.moveDown(side)
                elif command == "left":
                    game.AngleUp(side)
                elif command == "right":
                    game.AngleDown(side)
                elif command == "space":
                    game.throw(side)
                elif command == "collide":
                    game.collide(side)
                elif command == "quit":
                    game.stop()
            
            conn.send((side,game.get_info()))
    except:
        traceback.print_exc()
        conn.close()
    finally:
        print(f"Game ended {game}")


def main(ip_address):
    manager = Manager()
    try:
        with Listener((ip_address, 6000),
                      authkey=b'secret password') as listener:
            n_player = 0
            players = [None, None]
            game = Game(manager)
            while True:
                print(f"accepting connection {n_player}")
                conn = listener.accept()
                players[n_player] = Process(target=player,
                                            args=(n_player, conn, game))
                n_player += 1
                if n_player == 2:
                    players[0].start()
                    players[1].start()
                    n_player = 0
                    players = [None, None]
                    game = Game(manager)

    except Exception as e:
        traceback.print_exc()

if __name__=='__main__':
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]

    main(ip_address)