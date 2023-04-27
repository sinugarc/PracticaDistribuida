#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 10:03:19 2023

@author: alumno
"""

from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Value, Lock
import math
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

class Sword():
    def __init__(self, player):
        self.side=player
        self.pos=[-333,-333]
        self.velocity=[0,0]
        self.angle=0
        
    def update(self,dead):

        if self.pos != [-333,-333]:
            
            self.pos[X] += self.velocity[X]
            self.pos[Y] += self.velocity[Y]
            
            if self.pos[Y] > SIZE[Y] or self.pos[Y] < 0 or self.pos[X] < -50 or self.pos[X] > SIZE[X]+50:
                self.pos=[-333,-333]
                self.velocity=[0,0]
                self.angle=0
                dead = True
                
        return dead
            
    def throw(self,pos,ang):
        self.pos=pos
        self.angle=ang
        if self.side == 1:
            self.velocity[X]=-20*math.cos(ang*2*math.pi/360)
            self.velocity[Y]=20*math.sin(ang*2*math.pi/360)
        else:
            self.velocity[X]=20*math.cos(ang*2*math.pi/360)
            self.velocity[Y]=-20*math.sin(ang*2*math.pi/360)
        
   
class Target():
    def __init__(self,side):
        self.side=side
        if side==0:
            self.posx=SIZE[X]-16
            
        else:
            self.posx=-5
        self.posy=SIZE[Y]//2
        self.vel=2
        
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
        self.players = manager.list ( [Player(LEFT_PLAYER), Player(RIGHT_PLAYER)] )
        self.targets = manager.list ( [Target(LEFT_PLAYER), Target(RIGHT_PLAYER)] )
        self.swords= manager.list ( [Sword(LEFT_PLAYER),Sword(RIGHT_PLAYER)] )
        self.score = manager.list( [0,0] )
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
        p = self.players[player]
        if not p.thrown:
            pos = p.pos
            ang = p.angle
            s = self.swords[player]
            s.throw(pos, ang)
            self.swords[player] = s
            p.thrown = True
            self.players[player] = p
        self.lock.release()
   
    def targ(self,player):
        self.lock.acquire()
        t = self.targets[player]
        t.update()
        self.targets[player] = t
        self.lock.release()
        
    def swrd(self,player):
        self.lock.acquire()
        p = self.players[player]
        s = self.swords[player]
        dead = s.update(not p.thrown)
        p.thrown = not dead
        self.swords[player] = s
        self.players[player] = p
        self.lock.release()
    
    #Cambio score
    def collide(self,side):
        print('collide')
        self.lock.acquire()
        
        self.players[side].thrown=False
        
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
            'pos_left_sword': self.swords[LEFT_PLAYER].pos,
            'pos_right_sword': self.swords[RIGHT_PLAYER].pos,
            'angle_left_sword': self.swords[LEFT_PLAYER].angle,
            'angle_right_sword': self.swords[RIGHT_PLAYER].angle,
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
            if side==1:
                game.targ(1)
                game.targ(0)
                game.swrd(1)
                game.swrd(0)
            conn.send(game.get_info())
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