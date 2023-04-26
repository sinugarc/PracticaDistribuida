#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 10:03:19 2023

@author: alumno
"""

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
DELTA = 20
DELTA_2 = 10


class Player():
    def __init__(self, side):
        self.side = side
        if side == LEFT_PLAYER:
            self.pos = [70, SIZE[Y]//2]
        else:
            self.pos = [SIZE[X] - 70, SIZE[Y]//2]
        self.angle = 0
        self.thrown=False
        self.sword=Sword(side,[28,150],100,0)


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
    
    def throw(self):
        if not self.thrown:
            self.sword= Sword(self.side,self.pos,10, self.angle)
            self.thrown=True
        # return sw
    

class Sword():
    def __init__(self, side,playerpos,velocity,angle):
        self.side=side
        self.pos=playerpos
        self.velocity=velocity
        self.angle=angle
        
    def update(self):
        if self.side==0:
            self.pos[X] += self.velocity
            self.pos[Y] += self.velocity*self.angle/-100
        else:
            self.pos[X] -= self.velocity
            self.pos[Y] += self.velocity*self.angle/100
   
class Target():
    def __init__(self,side):
        self.side=side
        if side==0:
            self.posx=SIZE[X]-16
            
        else:
            self.posx=-5
        self.posy=SIZE[Y]//2
        self.vel=10
    def update(self):
        self.posy+=self.vel 
        if self.posy<0:
            self.posy=0
            self.vel*=-1
        if self.posy>SIZE[Y]:
            self.posy=SIZE[Y]
            self.vel*=-1
    

class Game():
    def __init__(self, manager):
        self.players = manager.list( [Player(LEFT_PLAYER), Player(RIGHT_PLAYER)] )
        self.targets = manager.list ( [Target(LEFT_PLAYER), Target(RIGHT_PLAYER)] )
        #self.swords= manager.list ([0,0])
        self.score = manager.list([0,0] )
        self.running = Value('i', 1) # 1 running
        self.lock = Lock()

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
        p=self.players[player]
        p.throw()
        self.players[player]=p
        self.lock.release()
   
    
    #Cambio score
    def collide(self,side):
        self.lock.acquire()
        
        self.players[side].thrown=False
        self.players[side].sword=0 #no iniciado
        
        a=self.score[side]
        a=a+1
        self.score[side]=a
    
        self.lock.release()
        
    #collide swords
        
    def get_info(self):
        info = {
            'pos_left_player': self.players[LEFT_PLAYER].pos,
            'pos_right_player': self.players[RIGHT_PLAYER].pos,
            'angle_left_player': self.players[LEFT_PLAYER].angle,
            'angle_right_player': self.players[RIGHT_PLAYER].angle,
            'pos_left_sword': self.players[LEFT_PLAYER].sword.pos,
            'pos_right_sword': self.players[RIGHT_PLAYER].sword.pos,
            'angle_left_sword': self.players[LEFT_PLAYER].sword.angle,
            'angle_right_sword': self.players[RIGHT_PLAYER].sword.angle,
            'pos_left_target': self.targets[LEFT_PLAYER].posy,
            'pos_right_target': self.targets[RIGHT_PLAYER].posy,
            'score': list(self.score),
            'is_running': self.running.value == 1
        }
        return info
   


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
                elif command == "collide": #collide entre swords
                    game.collide(side)
                elif command == "quit":
                    game.stop()
            game.targets[side].update()
            game.players[side].sword.update()
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