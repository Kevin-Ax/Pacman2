import sys

import pygame

from pacman.classes import Map
from pacman.settings import FPS, HEIGHT, WIDTH


class Game:
  def __init__(self):
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    self.clock = pygame.time.Clock()

    self.map = Map(self.screen)

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      self.screen.fill('black')
      self.map.run()

      pygame.display.update()
      self.clock.tick(FPS)


if __name__ == '__main__':
  game = Game()
  game.run()
