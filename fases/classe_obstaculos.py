import pygame
import random

class Obstaculo(pygame.sprite.Sprite): # classe pros obstáculos
    def __init__(self, chao_y):
        super().__init__()
        # lista de tipos de obstáculos 
        self.tipos = [
          pygame.image.load('imagens/pedra.png').convert_alpha(),
          pygame.image.load('imagens/arbusto.png').convert_alpha()
        ]
        #escolhe um tipo de obstáculo aleatoriamente
        self.image = random.choice(self.tipos)
        
        #muda o tamanho
        self.image = pygame.transform.scale(self.image, (32*3,32*3))

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
        self.rect.x = 1600  # fora da tela
        self.rect.y = self.chao_y - self.rect.height  # posição no chão

    def update(self, dt):
        # move o obstáculo para a esquerda
        self.rect.x -= self.velocidade_scroll * dt
        if self.rect.right < 0:
            # remove o obstáculo quando sair da tela (ajuda o jogo a n ficar pesado)
            self.kill()