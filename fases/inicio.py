import pygame
from pygame.locals import *
from sys import exit

def mostrar_inicio():
    pygame.init()
    largura = 1500
    altura = 700
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Jogo')

    estado = 'menu'

    imagem_inicio = pygame.image.load('imagens/inicio.png').convert()
    imagem_inicio = pygame.transform.scale(imagem_inicio, (largura, altura))
    botao = pygame.image.load('ferramentas/botãojogar.png').convert_alpha()
    botao = pygame.transform.scale(botao, (32*7, 32*7))
    botao_x = 650
    botao_y = 250
    botao_rect = botao.get_rect(topleft=(botao_x, botao_y))
    clock = pygame.time.Clock()
    while True:
        if estado == 'menu':
                tela.blit(imagem_inicio, (0,0))

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
               mouse_x, mouse_y = pygame.mouse.get_pos()
               if botao_rect.collidepoint(mouse_x, mouse_y):
                 print ("botão acionado")
                 if estado == 'menu':
                    return
                
        tela.blit(botao,(botao_x, botao_y))
        pygame.display.update()
        clock.tick(60)