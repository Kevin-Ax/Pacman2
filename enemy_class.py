from operator import truediv
import pygame
from settings import PLAYER_COLOUR, TOP_BOTTOM_BUFFER, WHITE, vec
import random
vec = pygame.math.Vector2

class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.radios = int(self.app.cell_width//2.3)
        self.number = number
        self.colour = self.set_colour()
        self.direction = vec(1,0)
        self.person = self.set_personality()
    
    def update(self):
        self.pix_pos = self.pix_pos + self.direction
        if self.time_tom_move():
            self.move()
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER+self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER+self.app.cell_height//2)//self.app.cell_height+1

    
    def draw(self):
        pygame.draw.circle(self.app.screen, self.colour, (int(self.pix_pos.x), int(self.pix_pos.y)), self.radios)
    
    def time_tom_move(self):
       pass
    
    def move(self):
        pass
            
    
    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
        (self.grid_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2+self.app.cell_height//2)
    
    def set_colour(self):
        if self.number == 0:
            return (43,78,203)
        if self.number == 1:
            return (197,200,27)
        if self.number == 2:
            return (169,29,29)
        if self.number == 3:
            return (215,155,35)
        
    def set_personality(self):
        if self.number == 0:
            return "speady"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scarred"