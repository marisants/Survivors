import pygame 
from pygame.locals import *

pygame.init()
gravidade = 2
class Personagem:
  def __init__(self, skin, nome, matricula, curso, largura, altura):
    self.__skin = skin
    self.__nome = nome
    self.__matricula = matricula
    self.__curso = curso
    @property
    def skin(self):
      return self.__skin
    @skin.setter
    def skin(self,skin):
      if skin == pygame.image.load("Survivors\imagens/.png").convert:
        self.__skin = skin
      else:
        return "personagem inválido"
        
    @property
    def nome(self):
      return self.__nome
    @nome.setter
    def nome(self, nome):
      if type(nome) == str:
        self.__nome = nome
      else:
        return "nome inválido"
    
    @property
    def matricula(self):
      return self.__matricula
    @matricula.setter
    def nome(self, matricula):
      if type(matricula) == int:
        self.__matricula = matricula
      else:
        return "nome inválido"
    @property
    def curso(self):
      return self.__curso
    @curso.setter
    def curso(self, curso):
      if type(curso) == str:
        self.__curso = curso
      else:
        return "curso inválido"
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