import pygame
from pygame.locals import *
from sys import exit
 
largura = 640
altura = 480

Branco = (0,0,0)

tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('teste')

sprite_sheet = pygame.image.load("imagens/avião.png").convert_alpha()

class Aviao(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.imagens = []
    for i in range(4):
      img = sprite_sheet.subsurface((i*64,0),(64,64))
      img = pygame.transform.scale(img,(64*3,64*3))
      self.imagens.append(img)
    self.index_lista = 0
    self.image = self.imagens[self.index_lista]
    self.rect = self.image.get_rect()
    self.rect.center = (100,100)
    
  def update(self):
    if self.index_lista >3:
      self.index_lista = 0
    self.index_lista += 0.25
    self.image = self.imagens[int(self.index_lista)]
    
  
todas_as_sprites = pygame.sprite.Group()

aviao = Aviao()
todas_as_sprites.add(aviao)

relogio = pygame.time.Clock()

while True:
  relogio.tick(30)
  tela.fill(Branco)
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      exit()
  todas_as_sprites.draw(tela)
  todas_as_sprites.update()
  
  pygame.display.flip()