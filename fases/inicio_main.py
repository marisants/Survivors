import pygame
from inicio import TelaInicio
from fase_1 import FaseUm
from fase_2 import FaseDois # importando a fase 2
from fase_3 import FaseTres # importando a fase 3
def main():
    pygame.init()
    tela = pygame.display.set_mode((1500, 700))
    
    # Criamos os objetos (instâncias das  classes) [1]
    menu = TelaInicio()
    fase1 = FaseUm()
    fase2 = FaseDois() #criando o obj da fase 2
    fase3 = FaseTres() #criando o obj da fase 3

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

        elif estado == "FASE3":
            resultado = fase3.jogar(tela)

            if resultado == "FASE_TERMINADA":
                estado = "FIM"
                
        pygame.display.flip()

if __name__ == '__main__':
    main()