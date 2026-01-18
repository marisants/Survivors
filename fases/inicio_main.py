import pygame
from inicio import TelaInicio
from fase_1 import FaseUm
from fase_2 import FaseDois # importando a fase 2
def main():
    pygame.init()
    tela = pygame.display.set_mode((1500, 700))
    
    # Criamos os objetos (instâncias das  classes) [1]
    menu = TelaInicio()
    fase1 = FaseUm()
    fase2 = FaseDois() #criando o obj da fase 2
    estado = "INICIO"
    rodando = True
    
    while rodando:
        if estado == "INICIO":
            # Se a função de início retornar que o botão foi clicado
            if menu.mostrar_inicio(tela):
                # Executa a transição antes de mudar de vez para a fase
                fase1.transicao_fade_in(tela)
                estado = "JOGAR"
    
    #mudei aqui p fazer a transição da fase1 pra fase 2
        elif estado == "JOGAR":
            resultado = fase1.jogar(tela)
            if resultado == "FASE_TERMINADA":
                estado = "FASE2"
                
        elif estado == "FASE2":
            fase2.jogar(tela)
            
        pygame.display.flip()

if __name__ == '__main__':
    main()