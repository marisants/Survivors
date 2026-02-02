import pygame
from pygame.locals import *
import math
import time
import random

from fases.classe_obstaculos import ObsfaseEasterEgg, Notapeba
from fases import funcoes
from fases.funcoes import tela_vitoria



class FaseEasterEgg:
    def __init__(self):
        self.brilho = 0
        self.superficie_fase = pygame.Surface((1500, 700)) # Ajuste ao seu tamanho

    def transicao_fade_in(self, tela_principal):
        while self.brilho < 255:
            self.brilho += 5
            if self.brilho > 255: self.brilho = 255
            
            # Desenha sua fase aqui dentro ou chama um método de desenho
            self.superficie_fase.fill((0, 0, 0)) # Exemplo: fase verde
            self.superficie_fase.set_alpha(self.brilho) # Define a transparência
            
            tela_principal.blit(self.superficie_fase, (0, 0))
            pygame.display.flip()
            time.sleep(0.02) # Soneca curta para suavizar [16.3.1] soneca?? KKKKKKKKK

    def jogar(self,tela):
        pygame.init()
        pygame.mixer.init()

        pygame.mixer.music.load("sons/1-02. Title.mp3")
        pygame.mixer.music.set_volume(0.3)  # volume entre 0.0 e 1.0
        pygame.mixer.music.play(-1)  # -1 = loop infinito

        #controla os frames por segundo do fundo
        clock = pygame.time.Clock()
        FPS = 50

        largura = 1500
        altura = 700 # define o tamanho da tela

        PRETO = (0,0,0)  # só uma variável pra botar o none e nao a cor
        pygame.display.set_caption("Survivors - Easter Egg")
        
        score = 0 # criando o score

        tempo_j = 0.0
        tempo_v = 20


        def exibir_pontuacao (textop, tamanho, cor): #função que vai exibir a pontuação na tela
            fonte = pygame.font.Font("ferramentas/HVD_Comic_Serif_Pro.otf", tamanho)
            mensagem = f'{textop}'
            mensagem_formatada = fonte.render(mensagem, True, cor)
            return mensagem_formatada
    
        #essa classe n era pra tá aq nn,era pra tá no arquivo da classe do personagem, mas td bem :)
        class Aluno(pygame.sprite.Sprite): # a segunda "Sprite" é uma classe q já é do pygame 
            def __init__(self):
                pygame.sprite.Sprite.__init__(self) # inicializa a classe 
                self.som_pulo = pygame.mixer.Sound("sons/pulando.wav")
                self.som_pulo.set_volume(1)
                #o do boneco correr
                self.sprites_correndo = [] # cria uma lista
                self.sprites_correndo.append(pygame.image.load('imagens/meninocorrer1.png'))
                self.sprites_correndo.append(pygame.image.load('imagens/meninocorrer2.png'))
                self.sprites_correndo.append(pygame.image.load('imagens/meninocorrer3.png'))
                self.sprites_correndo.append(pygame.image.load('imagens/meninocorrer4.png')) # só pra colocar as sprites
                
                #o do boneco agachar
                self.sprites_abaixando = [] # cria uma lista
                self.sprites_abaixando.append(pygame.image.load('imagens/agachar1.png'))
                self.sprites_abaixando.append(pygame.image.load('imagens/agachar2.png'))
                self.sprites_abaixando.append(pygame.image.load('imagens/agachar3.png'))
                self.sprites_abaixando.append(pygame.image.load('imagens/agachar4.png')) # só pra colocar as sprites
                
                #pra saber o estado do boneco
                self.estado = "andando"
                self.sprites = self.sprites_correndo # define as sprites iniciais como correndo

                self.atual = 0 # pra comecar da primeira imagem
                self.image = self.sprites[self.atual] # pra mudar
                self.image = pygame.transform.scale(self.image, (32*13, 32*13)) 

                #a merma coisa q eu botei no obst´culo p fazer a colisão certinha
                self.mask = pygame.mask.from_surface(self.image)

                self.rect = self.image.get_rect() # pega tipo as cordenadas de onde tá a imagem 
                self.rect.topleft = largura-1400, altura-480 # pra dzr a posição onde o boneco vai ficar

                self.pos_y_inicial = altura-400 # pra dzr onde o boneco tá antes de pular
                
                self.pulo = False
                self.vel_y = 0 #velocidade inicial do pulo
                self.gravidade_subida = 4500
                self.gravidade_descida = 5800  # mais forte pra baixar rápido (isso foi basicamente p arrumar o bixo baixando)
                self.forca_pulo = -1400 #o quanto que o boneco vai pular pra cima
                self.no_chao = True 
                
            def pular(self):
                if self.no_chao:
                    self.vel_y = self.forca_pulo # define a velocidade do pulo
                    self.no_chao = False
                    self.som_pulo.play()
                    
            def abaixar(self):
                if self.no_chao and self.estado == "andando":
                    self.estado = "abaixando"
                    self.sprites = self.sprites_abaixando
                    self.atual = 0

            def levantar(self):
                if self.estado in ("abaixado", "abaixando"):
                    self.estado = "andando"
                    self.sprites = self.sprites_correndo
                    self.atual = 0
  
            def update(self): # fzr update
                # gravidade
                if self.vel_y < 0:
                    self.vel_y += self.gravidade_subida * dt #isso é quando tá pulando
                else:
                    self.vel_y += self.gravidade_descida * dt #p descer mais rápido
                    
                self.rect.y += self.vel_y * dt # atualiza a posição do personagem
                    
                # fazer o personagem parar no chão
                if self.rect.y >= self.pos_y_inicial: 
                    self.rect.y = self.pos_y_inicial 
                    self.vel_y = 0
                    self.no_chao = True

                if self.estado == "abaixando":
                    self.atual += 9 * dt
                    if self.atual >= len(self.sprites_abaixando) - 1:
                        self.atual = len(self.sprites_abaixando) - 1
                        self.estado = "abaixado"

                elif self.estado == "andando":
                    self.atual += 9 * dt
                    if self.atual >= len(self.sprites):
                        self.atual = 0

                elif self.estado == "abaixado":
                    self.atual = len(self.sprites_abaixando) - 1

                base = self.rect.midbottom # pra manter o boneco n canto q tá quando abaixar

                self.image = self.sprites[int(self.atual)] # é pra poder botar número quebrado
                
                if self.estado in ("abaixado", "abaixando"):
                    self.image = pygame.transform.scale(self.image, (32*7, 32*7)) #ajusta o tamanho quando abaixa
                else:
                    self.image = pygame.transform.scale(self.image, (32*13, 32*13))  #se n tiver abaixado é o normal
                
                self.rect = self.image.get_rect(midbottom=base) #deixa o boneco no mermo lugar quando muda a sprite
                
                self.mask = pygame.mask.from_surface(self.image) #pro bixo da colisão funcionar certinho
                
                if self.no_chao:
                    if self.estado in ("abaixado", "abaixando"): 
                        self.rect.y = self.pos_y_inicial + 130 #faz o bixo baixar  no mrm chão que ele fica em pé
                    else:
                        self.rect.y = self.pos_y_inicial

        todas_as_sprites = pygame.sprite.Group() # cria um grupo pra tds as sprites
        obstaculos = pygame.sprite.Group() # cria um grupo pros obstáculos
        aluno = Aluno() # pra desenhar o aluno lá
        todas_as_sprites.add(aluno) # add aluno no grupo
        
        # carregar imagens do fundo
        imagem_fundo = pygame.image.load("imagens/fundo_ester_egg.jpeg").convert() # add a img de fundo
        imagem_fundo = pygame.transform.scale(imagem_fundo, (largura,altura)) # define o tamanho da img de fundo
        imagem_fundo_largura = imagem_fundo.get_width() # perguntar a mary (essas duas linhas servem pra ajustar o tamanho da imagem d fundo)
        tiles = math.ceil(largura / 700 ) #  perguntar a mary  (calcula o número de coisinho  pra cobrir a largura da tela)
        #rolagem lateral do fundo  e aumeto gradual da velocidade
        scroll = 0 
        velocidade_scroll = 100 #velocidade inicial da rolagem
        velocidade_maxima = 1500 
        aceleracao = 120 # o quanto a velocidade vai aumentar por segundo 
        
        tempo_spawn = 0 # tempo de nascimento dos obstáculos
        #controle de spawn dos obstáculos
        tempo_min_spawn = 0.6   # segundos 
        tempo_max_spawn = 1.2  # segundos
        proximo_tempo = random.uniform(tempo_min_spawn, tempo_max_spawn) # tempo aleatório entre os dois valores

        estado = "jogando"
        
        
        while True:
            #relogio.tick(20) # tempo
            dt = clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit() # é pra sair do jogo
                    exit() # pra fechar a janela

                if event.type == KEYDOWN and estado == "jogando": # pra n dar pra pular no game over
                    if event.key == K_SPACE: # pra só acontecer quando apertar na tecla do espaço
                        aluno.pular() 

                if event.type == KEYDOWN:
                  if event.key == K_DOWN:
                      aluno.abaixar()
                
                if event.type == KEYUP: # quando soltar a tecla
                    if event.key == K_DOWN:
                        aluno.levantar()

                #if estado == "vitoria":
                #    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                #        if botao_proximo_rect.collidepoint(event.pos):
                #            return "EASTER_COMPLETO"

            for i in range (tiles):
                tela.blit(imagem_fundo, (i * imagem_fundo_largura + scroll, 0 ))
            # atualiza o fundo
            if estado == "jogando":
                if velocidade_scroll < velocidade_maxima:
                    velocidade_scroll += aceleracao * dt
                elif velocidade_scroll > velocidade_maxima:
                    velocidade_scroll = velocidade_maxima

                scroll -= velocidade_scroll * dt
                tempo_j += dt
                
                #controle de spawn dos obstáculos por distância 
                if len(obstaculos) == 0 or list(obstaculos)[-1].rect.right < largura - 140:

                    # nascimento dos obstáculos
                    chance = random.randint(1, 5) #chandes de nascimento

                    if chance == 1:
                        # nasce avião
                        obstaculos.add(Notapeba(largura))
                    else:
                        # nasce ou teresa ou o banco
                        obstaculos.add(ObsfaseEasterEgg(altura - 50))

                 #reinicia o scroll mas não reseta a velocidade, se mantém a rolagem e a velocidade
                if abs(scroll) > imagem_fundo_largura:
                        scroll += imagem_fundo_largura

                todas_as_sprites.update() # faz o update
                todas_as_sprites.draw(tela) # dsenha sapo na tela (q sapo mulher?)
                obstaculos.update(dt) # update
                obstaculos.draw(tela) #desenha os obstáculos na tela

                #atualiza a velocidade dos obstáculos
                for obstaculo in obstaculos:
                    obstaculo.velocidade_scroll = min(velocidade_scroll, 800) # atualiza a velocidade do obstáculo conforme a velocidade do fundo
                # colisão só com os pixels visíveis
                if pygame.sprite.spritecollide(aluno, obstaculos, False, pygame.sprite.collide_mask):
                    return "GAME_OVER"

            if tempo_j >= tempo_v:
                return "EASTER_COMPLETO"

            
            #comando de voz próximo    
            if estado == "vitoria" and funcoes.comando_voz:
                if "próximo" in funcoes.comando_voz:
                    print("PRÓXIMO POR COMANDO DE VOZ")
                    funcoes.comando_voz = None
                    return "EASTER_COMPLETO"
          
            pygame.display.update() # processamennto 