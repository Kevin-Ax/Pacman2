import pygame

from pacman.settings import ROOT_DIR, TILE_SIZE
from pacman.utils import import_csv_layout

from .tile import Tile


class Map:
  def __init__(self, surface):
    # General setup
    self.level = {
      'grond': f'{ROOT_DIR}/pacman/assets/map_chao.csv',
      'walls': f'{ROOT_DIR}/pacman/assets/map_paredes.csv'
    }
    self.display_surface = surface

    # Terrain setup
    walls = import_csv_layout(self.level.get('walls', ''))
    self.walls_sprites = self.create_tile_group(walls, 'walls')

  def create_tile_group(self, layout, type):
    sprite_group = pygame.sprite.Group()

    for ridx, row in enumerate(layout):
      for cidx, col in enumerate(row):
        if col != '-1':
          x = cidx * TILE_SIZE
          y = ridx * TILE_SIZE

          if type == 'walls':
            sprite = Tile(TILE_SIZE, x, y)
            sprite_group.add(sprite)

    return sprite_group

  def run(self):
    self.walls_sprites.draw(self.display_surface)
