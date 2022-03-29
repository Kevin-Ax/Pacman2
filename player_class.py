import pygame

from settings import HEIGHT, PLAYER_COLOUR, TOP_BOTTOM_BUFFER, vec


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1,0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 3
        self.starting_pos = [pos.x, pos.y]

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move =  self.can_move()

        #trackeando o pixel do jogador
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER+self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER+self.app.cell_height//2)//self.app.cell_height+1

        if self.on_coin():
            self.eat_coin()

    def draw(self):
        pygame.draw.circle(self.app.screen, PLAYER_COLOUR,
        (int(self.pix_pos.x), int(self.pix_pos.y)),  self.app.cell_width//2-2)

        #desenhando retangulo rastreador do pixel do jogador
        # pygame.draw.rect(self.app.screen, RED,
        # (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
        # self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2,
        # self.app.cell_width, self.app.cell_height), 1)

        # Desenhando vida do pacman
        for i in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (30 + 20 * i, HEIGHT - 15), 7)

    def on_coin(self):
        return self.grid_pos in self.app.coins and \
            (int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0 or \
            int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0) and \
                (self.direction == vec(1, 0) or self.direction == (-1, 0) or \
                self.direction == vec(0, 1) or self.direction == (0, -1))

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
        (self.grid_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2+self.app.cell_height//2)

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1,0) or self.direction == vec(-1,0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0,1) or self.direction == vec(0,-1):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        return True
