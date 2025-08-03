import pygame
from pygame.locals import *
from sys import exit

pygame.init()
pygame.mixer.init()

largura = 640
altura = 480 # define o tamanho da tela

PRETO = (0,0,0)  # só uma variável pra botar o none e nao a cor

tela = pygame.display.set_mode((largura, altura)) # tb da tela
pygame.display.set_caption('Sprites')

class Aluno(pygame.sprite.Sprite): # a segunda "Sprite" é uma classe q já é do pygame 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # inicializa a classe 
        self.som_pulo = pygame.mixer.Sound("sons/pulando.wav")
        self.som_pulo.set_volume(1)
        self.sprites = [] # cria uma lista
        self.sprites.append(pygame.image.load('imagens/meninocorrer1.png'))
        self.sprites.append(pygame.image.load('imagens/meninocorrer2.png'))
        self.sprites.append(pygame.image.load('imagens/meninocorrer3.png'))
        self.sprites.append(pygame.image.load('imagens/meninocorrer4.png')) # só pra colocar as sprites

        self.atual = 0 # pra comecar da primeira imagem
        self.image = self.sprites[self.atual] # pra mudar
        self.image = pygame.transform.scale(self.image, (32*7, 32*7)) 

        self.rect = self.image.get_rect() # pega tipo as cordenadas de onde tá a imagem 
        self.rect.topleft = 50, 160 # pra dzr a posição onde o boneco vai ficar

        self.pos_y_inicial = 210 # pra dzr onde o boneco tá antes de pular
        self.pulo = False

    def pular(self):
         self.pulo = True 
         self.som_pulo.play()

    def update(self): # fzr update
            if self.pulo == True: # pra só se clicar no espaço acontecer as coisas 
                 if self.rect.y <= 200:
                      self.pulo = False
                 self.rect.y -= 50 # defie a posição q ele vai ficar na tela com o pulo
            else :
                if self.rect.y < self.pos_y_inicial:
                    self.rect.y += 50  # pra o boneco descer
                else :
                    self.rect.y = self.pos_y_inicial

            self.atual = self.atual + 0.5  # diminue a velocidade de andar
            if self.atual >= len(self.sprites): # pra se repetir , no caos de wuando acabar as sprits começa dnv
                self.atual = 0  
            self.image = self.sprites[int(self.atual)] # é pra poder botar número quebrado
            self.image = pygame.transform.scale(self.image, (32*7, 32*7)) # aumenta o tamanho da img , 128 é largura e 64 é altura 



todas_as_sprites = pygame.sprite.Group() # cria um grupo pra tds as sprites
aluno = Aluno() # pra desenhar o aluno lá
todas_as_sprites.add(aluno) # add aluno no grupoh

imagem_fundo = pygame.image.load("imagens/fundo_1.png").convert() # add a img de fundo
imagem_fundo = pygame.transform.scale(imagem_fundo,(largura,altura)) # define o tamanho da img de fundo

relogio = pygame.time.Clock() # diz a velocidade

while True:
    relogio.tick(30) # tempo
    tela.fill(PRETO)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() # é pra sair do progama 
            exit() # pra fechar a janela
        if event.type == KEYDOWN:
             if event.key == K_SPACE: # pra só acontecer quando apertar na tecla do espaço
                  if aluno.rect.y != aluno.pos_y_inicial: # pra n poder pular no ar
                    pass
                  else:
                   aluno.pular() # se ele tiver no chão aí pode pular
    
    tela.blit(imagem_fundo,(0,0)) # diz a posição onde a img vai ficar
    todas_as_sprites.draw(tela) # dsenha sapo na tela
    todas_as_sprites.update() # faz o upgrade
    pygame.display.flip() # processamennto