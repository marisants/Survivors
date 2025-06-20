import pygame 
from pygame.locals import *

pygame.init()
gravidade = 2
class Personagem:
  def __init__(self, skin, nome, matricula, curso, largura, altura):
    self.skin = skin
    self.nome = nome
    self.matricula = matricula
    self.curso = curso 
    self.altura = altura
    self.largura = largura
  def pular(self):
      for event in pygame.event.get():
        if event.type == KEYDOWN:
          if event.key == K_SPACE or K_UP:
            pass
  def abaixar(self):
    for event in pygame.event.get():
      if event.type == KEYDOWN: 
        if event.key == K_DOWN:
              pass
  