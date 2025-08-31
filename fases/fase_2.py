import pygame 
from pygame.locals import *
from sys import exit
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 120
largura = 1400
altura = 700
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo")

imagem_fundo = pygame.image.load("imagens/tela").convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (1400,700))
imagem_fundo_largura = imagem_fundo.get_width()
tiles = math.ceil(largura / 700 )

tempo_total = 0
scroll_ativo = True
scroll = 0 
velocidade_scroll = 100 
velocidade_maxima = 2000 
aceleracao = 150  
fade_img = pygame.Surface((largura,altura)).convert_alpha()
fade = fade_img.get_rect()
fade_img.fill((0,0,0))
fade_alpha = 0

while True:
  dt = clock.tick(FPS) / 1000
  tempo_total+= dt
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      exit()
      
  for i in range (0, tiles):
    tela.blit(imagem_fundo, (i * imagem_fundo_largura + scroll, 0 ))
    
  if tempo_total >=10:
    scroll_ativo = False
    tela.blit(fade_img, (0,0) )
    if fade_alpha<255:
      fade_alpha+=10
      fade_img.set_alpha(fade_alpha)
  if tempo_total>=11:
    scroll_ativo = True  
    imagem_fundo = pygame.image.load("Survivors\imagens/fundo_fase_3.png").convert()    
    tela.blit(imagem_fundo, fade)
    if fade_alpha == 255:
      fade_alpha-= 10
      
  if scroll_ativo: 
    if velocidade_scroll < velocidade_maxima:
      velocidade_scroll += aceleracao * dt
    elif velocidade_scroll > velocidade_maxima:
      velocidade_scroll = velocidade_maxima
    if abs(scroll) > imagem_fundo_largura:
      scroll += imagem_fundo_largura
    scroll -= velocidade_scroll * dt
  pygame.display.update()