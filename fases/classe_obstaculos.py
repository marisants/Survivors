import pygame
import random

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
        self.rect.x = random.randint(1800,2200) # fora da tela
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
    
    
#classes específicas para cada fase    
class Obs_fase1(Obstaculo):
    def __init__(self, chao_y):
        tipos = [
          pygame.image.load('imagens/pedra.png').convert_alpha(),
          pygame.image.load('imagens/arbusto.png').convert_alpha()
        ]
        super().__init__(chao_y, tipos)
        
class Obs_fase2(Obstaculo):
    def __init__(self, chao_y):
        tipos = [
          pygame.image.load('imagens/banco.png').convert_alpha(),
          pygame.image.load('imagens/teresa.png').convert_alpha()
        ]
        super().__init__(chao_y, tipos, escala=(32*6,32*6))
        
class Obs_fase3(Obstaculo):
    def __init__(self, chao_y):
        tipos = [
          pygame.image.load('imagens/lixeira.png').convert_alpha(),
          pygame.image.load('imagens/mochila.png').convert_alpha()
        ]
        super().__init__(chao_y, tipos)
        
class Obs_fase4(Obstaculo):
    def __init__(self, chao_y):
        tipos = [
          pygame.image.load('imagens/camera.png').convert_alpha(),
          pygame.image.load('imagens/cadeira.png').convert_alpha()
        ]
        super().__init__(chao_y, tipos)