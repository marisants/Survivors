import pygame
from pygame.locals import *
from sys import exit
import os

from personagem import Personagem
from background import Background

pygame.init()

LARGURA = 960
ALTURA = 540
AZUL = (135, 206, 235)
CHAO = 385

diretorio_principal = os.path.dirname(_file_)
diretorio_imagens = os.path.join(diretorio_principal, "sprite")

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo do IF")

spritesheet = pygame.image.load(os.path.join(diretorio_imagens, "spritesheet.png")).convert_alpha()
imagem_fundo = pygame.image.load(os.path.join(diretorio_imagens, "floresta.png"))

font_name = pygame.font.match_font('arial')

relogio = pygame.time.Clock()

tela_atual = "menu"
morreu = False

all_sprites = pygame.sprite.Group()
fundo = Background(imagem_fundo)
personagem = Personagem(spritesheet)
all_sprites.add(fundo)
all_sprites.add(personagem)

def fade_transition(tela, cor=(255, 105, 180), velocidade=45):
    fade = pygame.Surface((LARGURA, ALTURA))
    fade.fill(cor)
    for alpha in range(0, 256, velocidade):
        fade.set_alpha(alpha)
        tela.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(50)

while True:
    relogio.tick(60)
    tela.fill(AZUL)

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()

        if tela_atual == "menu":
            if evento.type == KEYDOWN:
                fade_transition(tela)  
                tela_atual = "jogo"

        elif tela_atual == "jogo":
            if evento.type == KEYDOWN:
                if evento.key == K_SPACE and not morreu:
                    personagem.pular()
                elif evento.key == K_f and not morreu:
                    personagem.morrer()
                    morreu = True
                elif evento.key == K_RETURN and morreu:
                    personagem = Personagem(spritesheet)
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(fundo)
                    all_sprites.add(personagem)
                    morreu = False

    if tela_atual == "menu":
        tela.fill((0, 0, 0))
        fonte = pygame.font.Font(font_name, 60)
        texto1 = fonte.render("Caos IFinito", True, (255, 255, 255))
        texto2 = fonte.render("Pressione qualquer tecla para começar", True, (255, 255, 255))
        tela.blit(texto1, (LARGURA // 2 - texto1.get_width() // 2, ALTURA // 2 - 80))
        tela.blit(texto2, (LARGURA // 2 - texto2.get_width() // 2, ALTURA // 2))

    elif tela_atual == "jogo":
        teclas = pygame.key.get_pressed()
        if not personagem.morrendo:
            if teclas[K_d] or teclas[K_LEFT]:
                personagem.vel_x = 5
            elif teclas[K_a] or teclas[K_RIGHT]:
                personagem.vel_x = -5
            else:
                personagem.vel_x = 0

        all_sprites.update()
        all_sprites.draw(tela)

        if morreu:
            fonte = pygame.font.Font(font_name, 60)
            texto1 = fonte.render("Você morreu", True, (0, 0, 0))
            texto2 = fonte.render("Pressione 'Enter' para reiniciar", True, (0, 0, 0))
            tela.blit(texto1, (LARGURA // 2 - texto1.get_width() // 2, ALTURA // 2 - 80))
            tela.blit(texto2, (LARGURA // 2 - texto2.get_width() // 2, ALTURA // 2))

    pygame.display.flip()