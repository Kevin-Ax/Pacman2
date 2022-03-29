import random
from enum import Enum
from operator import truediv
from typing import List, Optional

import numpy as np
import pygame

from settings import PLAYER_COLOUR, TOP_BOTTOM_BUFFER, WHITE, vec

vec = pygame.math.Vector2

class Enemy:
    class Personality(Enum):
        SPEEDY = 0
        SLOW = 1
        RANDOM = 2
        SCARRED = 3

    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.radios = int(self.app.cell_width//2.3)
        self.number = number
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.person = self.set_personality()

    def update(self):
        self.pix_pos = self.pix_pos + self.direction
        if self.time_to_move():
            self.move()
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER+self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER+self.app.cell_height//2)//self.app.cell_height+1

    def draw(self):
        pygame.draw.circle(self.app.screen, self.colour, (int(self.pix_pos.x), int(self.pix_pos.y)), self.radios)

    def time_to_move(self):
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def move(self):
        if self.person == self.Personality.RANDOM:
            self.direction = self.get_random_direction()
        else:
            self.direction = self.get_path_direction()

    def get_path_direction(self):
        next_cell = self.find_next_cell_in_path()
        x_dir = next_cell[0] - self.grid_pos[0]
        y_dir = next_cell[1] - self.grid_pos[1]
        return vec(x_dir, y_dir)

    def find_next_cell_in_path(self):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [int(self.app.player.grid_pos.x), int(self.app.player.grid_pos.y)])

        return path[1]

    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest



    def get_random_direction(self):
        grid_pos = self.grid_pos
        while True:
            number = random.random()
            if number < 0.25:
                x_dir, y_dir = 1, 0
            elif 0.25 <= number < 0.5:
                x_dir, y_dir = 0, 1
            elif 0.5 <= number < 0.75:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            dir_ = vec(x_dir, y_dir)
            if vec(int(dir_.x + grid_pos.x), int(dir_.y + grid_pos.y)) not in self.app.walls:
                return vec(x_dir, y_dir)


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
            return self.Personality.SPEEDY
        elif self.number == 1:
            return self.Personality.SLOW
        elif self.number == 2:
            return self.Personality.RANDOM
        else:
            return self.Personality.SCARRED
