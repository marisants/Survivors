import pygame
from pygame.locals import *
from sys import exit

def mostrar_inicio():
    pygame.init()
    largura = 1800
    altura = 700
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Jogo')

    estado = 'menu'

    imagem_inicio = pygame.image.load('SURVI.png').convert()
    imagem_inicio = pygame.transform.scale(imagem_inicio, (1800, 700))

    clock = pygame.time.Clock()
    while True:
        if estado == 'menu':
                tela.blit(imagem_inicio, (0,0))

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()

            if evento.type == KEYDOWN:
                if estado == 'menu' and evento.key == K_RETURN:
                    return
            
        pygame.display.update()
        clock.tick(60)