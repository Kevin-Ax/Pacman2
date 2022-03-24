from csv import reader
from settings import TILE_SIZE
import pygame
from os import walk 

def import_foler(path):
  for information in walk(path):
    print(information)

def import_csv_layout(path: str):
  terrain = []
  with open(path) as map:
    layout = reader(map, delimiter=',')
    for row in layout:
      terrain.append(list(row))
  return terrain

def import_cut_graphics(path):
  surface = pygame.image.load(path).convert_alpha()
  tile_num_x = int(surface.get_size()[0] / TILE_SIZE)
  tile_num_y = int(surface.get_size()[1] / TILE_SIZE)
  
  cut_tiles = []
  for row in range(tile_num_y):
    for col in range(tile_num_x):
      x = col * TILE_SIZE
      y = row * TILE_SIZE
      new_surfc = pygame.Surface((TILE_SIZE,TILE_SIZE))
      new_surfc.blit(surface,(0,0),pygame.Rect(x,y,TILE_SIZE,TILE_SIZE))
      cut_tiles.append(new_surfc)
      
  return cut_tiles
  
