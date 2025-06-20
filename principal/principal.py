import pygame 
from pygame.locals import *
from sys import exit
#from classe_obstaculos import Obstaculos
#from classe_personagem_1 import Persongem_1
#from classe_personagem_2 import Personagem_2
from fases.fase_1 import Fase_1
#from fase_2 import fase_2
#from fase_3 import fase_3
#from fase_4 import fase_4

pygame.init()

largura = 640
altura = 480

tela = pygame.display.set_mode((largura, altura ))
pygame.display.set_caption ("jogo")

while True:
  tela.fill ((0,0,0))
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      exit()
  pygame.display.update()