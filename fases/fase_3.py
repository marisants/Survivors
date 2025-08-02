import pygame 
from pygame.locals import *
from sys import exit
import math

pygame.init()
#controlar os FPS do jogo
clock = pygame.time.Clock()
FPS = 120
#tela 
largura = 1800
altura = 700
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo")
#imagem de fundo da fase 
imagem_fundo = pygame.image.load("imagens/fundo_3.png").convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (1400,700))
imagem_fundo_largura = imagem_fundo.get_width()
tiles = math.ceil(largura / 700 )
#rolagem lateral do fundo  e aumeto gradual da velocidade
scroll = 0 
velocidade_scroll = 100 #velocidade inicial da rolagem
velocidade_maxima = 2000 
aceleracao = 150 # o quanto a velocidade vai aumentar por segundo 
while True:
  dt = clock.tick(FPS) / 1000
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      exit()
  for i in range (0, tiles):
    tela.blit(imagem_fundo, (i * imagem_fundo_largura + scroll, 0 ))
  if velocidade_scroll < velocidade_maxima:
    velocidade_scroll += aceleracao * dt
  elif velocidade_scroll > velocidade_maxima:
    velocidade_scroll = velocidade_maxima
  
  scroll -= velocidade_scroll * dt
  #reinicia o scroll mas não reseta a velocidade, se mantém a rolagem e a velocidade
  if abs(scroll) > imagem_fundo_largura:
    scroll = 0 
  pygame.display.update()