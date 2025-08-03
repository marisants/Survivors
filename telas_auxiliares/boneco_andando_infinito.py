import pygame
from pygame.locals import *
from sys import exit

pygame.init()

largura = 640
altura = 480 # define o tamanho da tela

PRETO = (0,0,0)  # só uma variável pra botar o none e nao a cor

tela = pygame.display.set_mode((largura, altura)) # tb da tela
pygame.display.set_caption('Sprites')

class Aluno(pygame.sprite.Sprite): # a segunda "Sprite" é uma classe q já é do pygame 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # inicializa a classe 
        self.sprites = [] # cria uma lista
        self.sprites.append(pygame.image.load('imagens/meninocorrer1.png'))
        self.sprites.append(pygame.image.load('imagens/meninocorrer2.png'))
        self.sprites.append(pygame.image.load('imagens/meninocorrer3.png'))
        self.sprites.append(pygame.image.load('imagens/meninocorrer4.png')) # só pra colocar as sprites

        self.atual = 0 # pra comecar da primeira imagem
        self.image = self.sprites[self.atual] # pra mudar
        self.image = pygame.transform.scale(self.image, (32*7, 32*7))

        self.rect = self.image.get_rect() # pega tipo as cordenadas de onde tá a imagem 
        self.rect.topleft = 100, 100 # pra dzr a posição onde o boneco vai ficar

    def update(self): # fzr update
            self.atual = self.atual + 0.5  # diminue a velocidade
            if self.atual >= len(self.sprites): # pra se repetir , no caos de wuando acabar as sprits começa dnv
                self.atual = 0  
            self.image = self.sprites[int(self.atual)] # é pra poder botar número quebrado
            self.image = pygame.transform.scale(self.image, (32*7, 32*7)) # aumenta o tamanho da img , 128 é largura e 64 é altura 



todas_as_sprites = pygame.sprite.Group() # cria um grupo pra tds as sprites
aluno = Aluno() # pra desenhar o aluno lá
todas_as_sprites.add(aluno) # add aluno no grupoh

relogio = pygame.time.Clock() # diz a velocidade

while True:
    relogio.tick(30) # tempo
    tela.fill(PRETO)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() # é pra sair do progama 
            exit() # pra fechar a janela
    
    todas_as_sprites.draw(tela) # dsenha sapo na tela
    todas_as_sprites.update() # faz o upgrade
    pygame.display.flip() # processamennto