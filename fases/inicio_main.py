import pygame
from inicio import TelaInicio
from fase_1 import FaseUm

def main():
    pygame.init()
    tela = pygame.display.set_mode((1500, 700))
    
    # Criamos os objetos (instâncias das  classes) [1]
    menu = TelaInicio()
    fase1 = FaseUm()
    
    estado = "INICIO"
    rodando = True
    
    while rodando:
        if estado == "INICIO":
            # Se a função de início retornar que o botão foi clicado
            if menu.mostrar_inicio(tela):
                # Executa a transição antes de mudar de vez para a fase
                fase1.transicao_fade_in(tela)
                estado = "JOGAR"
        
        elif estado == "JOGAR":
            fase1.jogar(tela)
            
        pygame.display.flip()

if __name__ == '__main__':
    main()