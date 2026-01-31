import pygame
from pygame.locals import *
from sys import exit
import math
import time 
from classe_obstaculos import Obs_fase3, Aviao #importando a classe dos obstáculos dessa fase
import random #importando a biblioteca para gerar números aleatórios
import funcoes
from funcoes import tela_pause, tela_vitoria, comando_voz


class FaseTres:
    def __init__(self):
        self.brilho = 0
        self.superficie_fase = pygame.Surface((1500, 700)) # tamanho da "tela de transição"

    def transicao_fade_in(self, tela_principal):
        while self.brilho < 255: # essas 3 linhas muda o brilho pra dar a impressão de ir aparecendo
            self.brilho += 5
            if self.brilho > 255: self.brilho = 255
            
            # Desenha a fase aqui dentro ou chama um método de desenho
            self.superficie_fase.fill((0, 0, 0)) # Exemplo: fase preta
            self.superficie_fase.set_alpha(self.brilho) # Define a transparência , pra ir aarecendo devagar
            
            tela_principal.blit(self.superficie_fase, (0, 0))
            pygame.display.flip()
            time.sleep(0.02) # Soneca curta para suavizar [16.3.1] soneca?? KKKKKKKKK
            #é , a tela tipo demora um tantin pra aparecer

    def jogar(self,tela):
        pygame.init()
        pygame.mixer.init()

        pygame.mixer.music.load("sons/1-02. Title.mp3")
        pygame.mixer.music.set_volume(0.3)  # diz o volume e só pd de 0.0 a 1.0
        pygame.mixer.music.play(-1)  # deixa tocand sempre

        #controla os frames por segundo do fundo
        clock = pygame.time.Clock()
        FPS = 50

        largura = 1500
        altura = 700 # define o tamanho da tela

        PRETO = (0,0,0)  # só uma variável pra botar o none e nao a cor

        tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Survivors - Fase 3") 


        gameover_img = pygame.image.load("ferramentas/gameover2.png").convert_alpha()
        gameover_img = pygame.transform.scale(gameover_img, (850, 200))  # ajusta o tamanho
        gameover_rect = gameover_img.get_rect(center=(750, 200))
        
        botao_reiniciar = pygame.image.load("ferramentas/reiniciar2.png").convert_alpha()
        botao_reiniciar = pygame.transform.scale(botao_reiniciar, (400, 100))  # ajusta o tamanho
        botao_reiniciar_rect = botao_reiniciar.get_rect(center=(750, 390))

        botao_proximo = pygame.image.load("ferramentas/reiniciar2.png").convert_alpha()
        botao_proximo = pygame.transform.scale(botao_proximo, (400, 100))  # ajusta o tamanho
        botao_proximo_rect = botao_proximo.get_rect(center=(750, 510))

        score = 1400 # aqui coloca o limite que foi pra passar da fase 2

        pontuacao_final = None # só pra dzr q ainda n tem valor , mas n é 0

        tempo_j = 0.0
        tempo_v = 20

        def resetar_jogo():
                #essa próxima vai dzr q vai modificar essas variáveias aq dentro , mas q elas são de fora
                nonlocal score, velocidade_scroll, scroll, estado, musica_gameover_tocando , aluno , pontuacao_final, tempo_j
                pontuacao_final = None # tb só pra dzr q n tem valor ainda , mas agr é validado

                score = 0 # zera a pontuação
                velocidade_scroll = 100 # volta a velocidade do início do jogo
                scroll = 0 # volta a rolagem do fundo , pra n ir de onde parou
                musica_gameover_tocando = False # tipo para a música do game over
                estado = "jogando" # sai do game over pra voltar pro jogo
                tempo_j = 0.0

                obstaculos.empty() #apaga os obstáculos antigos 

                todas_as_sprites.empty() # apaga o boneco antigo
                aluno = Aluno() # atualiza o aluno principal
                todas_as_sprites.add(aluno) # desenha esse boneco na tela

                pygame.mixer.music.stop() # pra qualquer música
                pygame.mixer.music.load("sons/1-02. Title.mp3") # só pega a música salva 
                pygame.mixer.music.set_volume(0.3) # volume
                pygame.mixer.music.play(-1) # ficar voltando a música se terminar

        # ransforma texto em img
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
                # o do boneco correr
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

                self.pos_y_inicial = altura-480 # pra dzr onde o boneco tá antes de pular
                
                self.pulo = False
                self.vel_y = 0 #velocidade inicial do pulo
                self.gravidade = 4500 #força da gravidade
                self.forca_pulo = -1400 #o quanto que o boneco vai pular pra cima
                self.no_chao = True 
                
            def pular(self):
                if self.no_chao:
                    self.vel_y = self.forca_pulo # define a velocidade do pulo
                    self.no_chao = False
                    self.som_pulo.play()

            def abaixar(self):
                if self.no_chao:
                  self.estado = "abaixado"
                  self.sprites = self.sprites_abaixando
                  self.atual = 0

            def levantar(self):
                if self.estado == "abaixado":
                    self.estado = "andando"
                    self.sprites = self.sprites_correndo
                    self.atual = 0
            

            def update(self): # fzr update
                # gravidade
                self.vel_y += self.gravidade * dt # aceleração da gravidade
                self.rect.y += self.vel_y * dt # atualiza a posição do personagem
                    
                # fazer o personagem parar no chão
                if self.rect.y >= self.pos_y_inicial: 
                    self.rect.y = self.pos_y_inicial 
                    self.vel_y = 0
                    self.no_chao = True

                self.atual += 9 * dt # controla a velocidade da troca das sprites (cm eu tirei os dois relógio e deixei só um ai teve q mudar isso)
                if self.atual >= len(self.sprites): # pra se repetir , no caso de quando acabar as sprits começa dnv
                    self.atual = 0  
                self.image = self.sprites[int(self.atual)] # é pra poder botar número quebrado
                self.image = pygame.transform.scale(self.image, (32*13, 32*13)) # aumenta o tamanho da img , a primeira é largura e a segunda é altura
            
                base = self.rect.midbottom # pra manter o boneco n canto q tá quando abaixar

                self.image = self.sprites[int(self.atual)] # é pra poder botar número quebrado
                
                if self.estado == "abaixado":
                    self.image = pygame.transform.scale(self.image, (32*7, 32*7)) #ajusta o tamanho quando abaixa
                else:
                    self.image = pygame.transform.scale(self.image, (32*13, 32*13))  #se n tiver abaixado é o normal
                
                self.rect = self.image.get_rect(midbottom=base) #deixa o boneco no mermo lugar quando muda a sprite
                
                self.mask = pygame.mask.from_surface(self.image) #pro bixo da colisão funcionar certinho
                
                if self.no_chao:
                    if self.estado == "abaixado": 
                        self.rect.y = self.pos_y_inicial + 130 #faz o bixo baixar  no mrm chão que ele fica em pé
                    else:
                        self.rect.y = self.pos_y_inicial
                            

            #faz a tela d gameover aparecer
            def morrer(self): # é um método da classe aluno e só é chamado o estado = game over
                tela.blit(gameover_img, gameover_rect) # bota a img no canto crt

                if pontuacao_final: # se tiver pontuação final
                    tela.blit(
                        pontuacao_final,
                        pontuacao_final.get_rect(center=(750, 500))
                    ) # tudo acima desenha a pontuação
                #coisa do botão
                tela.blit(botao_reiniciar, botao_reiniciar_rect)

        todas_as_sprites = pygame.sprite.Group() # cria um grupo pra tds as sprites
        obstaculos = pygame.sprite.Group() # cria um grupo pros obstáculos
        aluno = Aluno() # pra desenhar o aluno lá
        todas_as_sprites.add(aluno) # add aluno no grupo
        
        # carregar imagens do fundo
        imagem_fundo = pygame.image.load("imagens/fundo_3.png").convert() # add a img de fundo
        imagem_fundo = pygame.transform.scale(imagem_fundo, (largura,altura)) # define o tamanho da img de fundo
        imagem_fundo_largura = imagem_fundo.get_width() # perguntar a mary (essas duas linhas servem pra ajustar o tamanho da imagem d fundo)
        tiles = math.ceil(largura / 700 ) #  perguntar a mary  (calcula o número de coisinho  pra cobrir a largura da tela)
        #rolagem lateral do fundo  e aumeto gradual da velocidade
        scroll = 0 
        velocidade_scroll = 200 #velocidade inicial da rolagem
        velocidade_maxima = 1500 
        aceleracao = 200 # o quanto a velocidade vai aumentar por segundo 
        
        distancia_spawn = 0 # distância dos nascimentos dos obstáculos
        #controle de spawn dos obstáculos
        proximo_spawn = random.randint(900, 1200)
        
        tempo_spawn = 0 # tempo de nascimento dos obstáculos
        #controle de spawn dos obstáculos
        tempo_min_spawn = 0.6   # segundos 
        tempo_max_spawn = 1.2  # segundos
        proximo_tempo = random.uniform(tempo_min_spawn, tempo_max_spawn) # tempo aleatório entre os dois valores
        
        musica_gameover_tocando = False
        pausado = False

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

                    if event.key == pygame.K_ESCAPE  and not pausado :
                        pausado = True
                    elif event.key == pygame.K_ESCAPE and pausado:
                        pausado = False 
                        
                if estado == "gameover":
                    if event.type == MOUSEBUTTONDOWN and event.button == 1: # só funciona se apertar o botão esquerou ou os dois do mouse 
                        if botao_reiniciar_rect.collidepoint(event.pos): # pra saber se o clique foi na área que o botão foi desenhado 
                           resetar_jogo()
                if estado == "vitoria":
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        if botao_reiniciar_rect.collidepoint(event.pos):
                            resetar_jogo()
                        if botao_proximo_rect.collidepoint(event.pos):
                            return "FASE_TERMINADA"

            #comando de voz reiniciar
            if estado == "gameover" and funcoes.comando_voz:
                if "jogar de novo" in funcoes.comando_voz:
                    print("REINICIANDO POR VOZ")
                    funcoes.comando_voz = None  # limpa pra não repetir
                    resetar_jogo()
                        
            if pausado:
                tela_pause (tela, pontuacao)
                pygame.display.flip()
                continue

        
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
                    chance = random.randint(1, 5) #chandes de nascimento

                    if chance == 1:
                        # nasce avião
                        obstaculos.add(Aviao(largura))
                    else:
                        # nasce ou teresa ou o banco
                        obstaculos.add(Obs_fase3(altura - 150))
                    
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

                    if not musica_gameover_tocando:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("sons/04_Game Over (SID Stereo).mp3")
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.play(-1)
                        musica_gameover_tocando = True

                    pontuacao_final = exibir_pontuacao(
                        f"Pontos finais: {score}", 60, (0,0,0)
                    ) # pelo q entendi é pra pontuação variar , n ser fixa
                     # e imprime cm uma img , n cm número

                    estado = "gameover"

                else:
                    score += int(100 * dt)
                    pontuacao = exibir_pontuacao(score, 50, (0,0,0))
                    tela.blit(pontuacao, (1300, 30))
 
            elif estado == "gameover":
                aluno.morrer()
            
            elif estado == "vitoria":
                tela_vitoria(tela, pontuacao)
 
            if tempo_j >= tempo_v:
                estado = "vitoria" 
                
            #comando de voz próximo    
            if estado == "vitoria" and funcoes.comando_voz:
                if "próximo" in funcoes.comando_voz:
                    print("PRÓXIMO POR COMANDO DE VOZ")
                    funcoes.comando_voz = None
                    return "FASE_TERMINADA"   
                if "jogar de novo" in funcoes.comando_voz:
                    print("RENICIAR POR COMANDO DE VOZ")
                    resetar_jogo() 
                
            pygame.display.update() # processamennto 