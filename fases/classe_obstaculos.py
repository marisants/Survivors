import pygame
import random
import os #importei essa bixa pq tava dando erro na importação das imagens por causa do diretório
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) #descobre a "pasta mãe " do projeto 
IMG_DIR = os.path.join(BASE_DIR, "imagens") #define um diretorio base pras imagens 

class Obstaculo(pygame.sprite.Sprite): # classe pros obstáculos
    def __init__(self, chao_y, tipos, escala=(32*3,32*3)):
        super().__init__()
        
        self.tipos = tipos
        #escolhe um tipo de obstáculo aleatoriamente
        self.image = random.choice(self.tipos)
        
        #muda o tamanho
        self.image = pygame.transform.scale(self.image, escala)
        #pega tipo o retângulo do obstáculo
        self.rect = self.image.get_rect()
        
        #cria a máscara pra colisão funcionar só com os pixels q a gnt vê
        self.mask = pygame.mask.from_surface(self.image)
        
        # velocidade de scroll do obstáculo
        self.velocidade_scroll = 300
        
        # posição y do chão
        self.chao_y = chao_y
        
        # cria o obstáculo
        self.criacao()

    def criacao(self):
        self.rect.x = random.randint(1650,2400) # fora da tela
        self.rect.y = self.chao_y - self.rect.height  # posição no chão

    def update(self, dt):

        # limita a velocidade do obstáculo (evita obstáculos impossíveis)
        velocidade = min(self.velocidade_scroll, 1100)
        #valor = randon.randint(0, 300)

        # move o obstáculo
        self.rect.x -= (velocidade * dt)

        # remove quando sair da tela
        if self.rect.right < 0:
            self.kill()
            
        self.rect.y = self.chao_y - self.rect.height
    
#classe para o avião
class Aviao(pygame.sprite.Sprite):
    def __init__(self, largura):
        super().__init__()
        self.aviao = pygame.image.load(os.path.join(IMG_DIR, "aviao.png")).convert_alpha() #tive que mudar todos os bixo dos obstáculos p usar a bixa q eu importei lá em cima e n dar erro
        self.imagens_aviao = [] #lista de imagens da spritesheet do aviao
        for i in range(4): #quantidade de sprites da animação
            img = self.aviao.subsurface((i*64, 0, 64, 64)) #diz qual imagem é 
            img = pygame.transform.scale(img, (64*3, 64*3)) #muda o tamanho
            self.imagens_aviao.append(img) #adiciona a lista

        self.index_lista = 0 #diz o indice da lista que começa a animação
        self.image = self.imagens_aviao[self.index_lista] #define a imagem da animação
        self.rect = self.image.get_rect() #pega oretângulo da imagem
        self.rect.x = largura + random.randint(200, 600) #escolhe aleatoriamente o canto q vai nascer 
        self.rect.y = 250 # altura

        self.mask = pygame.mask.from_surface(self.image) #máscara p facilitar colisão
        self.velocidade_scroll = 0 # p acompanhar  a velocidade do fundo

    def update(self, dt):
        # movimento
        self.rect.x -= self.velocidade_scroll * dt
        # animação
        self.index_lista += 6 * dt #faz rodar a animação
        if self.index_lista >= len(self.imagens_aviao):
            self.index_lista = 0
        self.image = self.imagens_aviao[int(self.index_lista)]

        # remove da tela
        if self.rect.right < 0:
            self.kill()
#classe para o capelo
class Capelo(pygame.sprite.Sprite):
    def __init__(self, largura):
        super().__init__()
        self.capelo = pygame.image.load(os.path.join(IMG_DIR, "capelo.png")).convert_alpha() #tive que mudar todos os bixo dos obstáculos p usar a bixa q eu importei lá em cima e n dar erro
        self.imagens_capelo = [] #lista de imagens da spritesheet do aviao
        for i in range(4): #quantidade de sprites da animação
            img = self.capelo.subsurface((i*64, 0, 64, 64)) #diz qual imagem é 
            img = pygame.transform.scale(img, (64*3, 64*3)) #muda o tamanho
            self.imagens_capelo.append(img) #adiciona a lista

        self.index_lista = 0 #diz o indice da lista que começa a animação
        self.image = self.imagens_capelo[self.index_lista] #define a imagem da animação
        self.rect = self.image.get_rect() #pega oretângulo da imagem
        self.rect.x = largura + random.randint(200, 600) #escolhe aleatoriamente o canto q vai nascer 
        self.rect.y = 200 # altura

        self.mask = pygame.mask.from_surface(self.image) #máscara p facilitar colisão
        self.velocidade_scroll = 0 # p acompanhar  a velocidade do fundo

    def update(self, dt):
        # movimento
        self.rect.x -= self.velocidade_scroll * dt
        # animação
        self.index_lista += 6 * dt #faz rodar a animação
        if self.index_lista >= len(self.imagens_capelo):
            self.index_lista = 0
        self.image = self.imagens_capelo[int(self.index_lista)]

        # remove da tela
        if self.rect.right < 0:
            self.kill()
#classes específicas para cada fase    
class Obs_fase1(Obstaculo):
    def __init__(self, chao_y):
        tipos = [
          pygame.image.load(os.path.join(IMG_DIR, "pedra.png")).convert_alpha(),
          pygame.image.load(os.path.join(IMG_DIR, "arbusto.png")).convert_alpha()
        ]
        super().__init__(chao_y, tipos)
        
class Obs_fase2(Obstaculo):
    def __init__(self, chao_y):
        tipos = [
          pygame.image.load(os.path.join(IMG_DIR, "banco.png")).convert_alpha(),
          pygame.image.load(os.path.join(IMG_DIR, "teresa.png")).convert_alpha()
        ]
        if random.randint(1, 200) == 1: # p o avião aparecer 1 em 200 vezes q roda o código (FPS)
            self.obstaculos.add(Aviao(self.largura))
        super().__init__(chao_y, tipos, escala=(32*6,32*6))
        
class Obs_fase3(Obstaculo):
    def __init__(self, chao_y):
        tipos = [
          pygame.image.load(os.path.join(IMG_DIR, "lixeira.png")).convert_alpha(),
          pygame.image.load(os.path.join(IMG_DIR, "mochila.png")).convert_alpha()
        ]
        if random.randint(1, 200) == 1: # p o avião aparecer 1 em 200 vezes q roda o código (FPS)
            self.obstaculos.add(Aviao(self.largura))
        super().__init__(chao_y, tipos, escala = (32*5, 32*5))
        
class Obs_fase4(Obstaculo):
    def __init__(self, chao_y):
        tipos = [
          pygame.image.load(os.path.join(IMG_DIR, "camera.png")).convert_alpha(),
          pygame.image.load(os.path.join(IMG_DIR, "banco.png")).convert_alpha()
        ]
        if random.randint(1, 200) == 1: # p o avião aparecer 1 em 200 vezes q roda o código (FPS)
            self.obstaculos.add(Aviao(self.largura))
        super().__init__(chao_y, tipos, escala = (32*6, 32*6))