import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from inicio import TelaInicio
from fase_1 import FaseUm
from fase_2 import FaseDois # importando a fase 2
from fase_3 import FaseTres # importando a fase 3
from fase_4 import FaseQuatro # importando a fase 3
from easter_egg.easter_egg import FaseEasterEgg


def main():
    pygame.init()
    tela = pygame.display.set_mode((1500, 700))
    
    # Criamos os objetos (instâncias das  classes) [1]
    menu = TelaInicio()
    fase1 = FaseUm()
    fase2 = FaseDois() #criando o obj da fase 2
    fase3 = FaseTres() #criando o obj da fase 3
    fase4 = FaseQuatro() #criando o obj da fase 3
    fase_easter = FaseEasterEgg()



    estado = "INICIO"
    rodando = True
    
    while rodando:

        if estado == "INICIO":
            if menu.mostrar_inicio(tela):
                fase1.transicao_fade_in(tela)
                estado = "FASE1"

        elif estado == "FASE1":
            resultado = fase1.jogar(tela)

            if resultado == "FASE_TERMINADA":
                fase2.transicao_fade_in(tela)
                estado = "FASE2"

        elif estado == "FASE2":
            resultado = fase2.jogar(tela)

            if resultado == "FASE_TERMINADA":
                fase3.transicao_fade_in(tela)
                estado = "FASE3"

            elif resultado == "EASTER_EGG":
                fase_easter.transicao_fade_in(tela)
                estado = "EASTER"

        elif estado == "EASTER":
            resultado = fase_easter.jogar(tela)

            if resultado == "EASTER_COMPLETO":
                fase4.transicao_fade_in(tela)
                estado = "FASE4"

            elif resultado == "GAME_OVER":
                fase2.transicao_fade_in(tela)
                estado = "FASE2"

        elif estado == "FASE3":
            resultado = fase3.jogar(tela)

            if resultado == "FASE_TERMINADA":
                fase4.transicao_fade_in(tela)
                estado = "FASE4"

        elif estado == "FASE4":
            resultado = fase4.jogar(tela)
            if resultado == "FASE_1":
                fase1 = FaseUm()
                fase1.jogar(tela)

            if resultado == "FASE_TERMINADA":
                estado = "FIM"
                
        pygame.display.flip()

if __name__ == '__main__':
    main()