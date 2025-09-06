import pygame
from pygame.locals import *
from sys import exit
import math

def jogar():
    pygame.init()
    pygame.mixer.init()

    #controla os fraes por segundo do fundo
    clock = pygame.time.Clock()
    FPS = 50

    largura = 1500
    altura = 700 # define o tamanho da tela

    PRETO = (0,0,0)  # só uma variável pra botar o none e nao a cor

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Sprites")

    cacto = pygame.image.load('imagens/cacto.png').convert_alpha() #criando o cacto
    cacto = pygame.transform.scale(cacto, (32*7, 32*7)) 
    cacto_rect = cacto.get_rect() #criando o retangulo do cacto
    x = largura + 200
    y = (altura - 100) - cacto.get_height() # pra ele ficar no mesmo chão do boneco
    
    fonte = pygame.font.Font("ferramentas/HVD_Comic_Serif_Pro.otf", 40) #criando uma fonte
    gameover_img = pygame.image.load("ferramentas/gameover.png").convert_alpha()
    gameover_img = pygame.transform.scale(gameover_img, (800, 400))  # ajusta o tamanho
    gameover_rect = gameover_img.get_rect(center=(800, 300))
    
    botao_reiniciar = pygame.image.load("ferramentas/reiniciar.png").convert_alpha()
    botao_reiniciar = pygame.transform.scale(botao_reiniciar, (400, 200))  # ajusta o tamanho
    botao_reiniciar_rect = gameover_img.get_rect(center=(950, 500))
    
    botao_mapa = pygame.image.load("ferramentas/mapavermelho.png").convert_alpha()
    botao_mapa = pygame.transform.scale(botao_mapa, (400, 200))  # ajusta o tamanho
    botao_mapa_rect = gameover_img.get_rect(center=(950, 600))
    score = 0 # criando o score
    def exibir_pontuacao (textop, tamanho, cor): #função que vai exibir a pontuação na tela
        fonte = pygame.font.Font("ferramentas/HVD_Comic_Serif_Pro.otf", tamanho)
        mensagem = f'{textop}'
        mensagem_formatada = fonte.render(mensagem, True, cor)
        return mensagem_formatada
    #essa classe n era pra tá aq nn,era pra tá no arquvio da classe do personagem, mas td bem :)
    class Aluno(pygame.sprite.Sprite): # a segunda "Sprite" é uma classe q já é do pygame 
        def __init__(self):
            pygame.sprite.Sprite.__init__(self) # inicializa a classe 
            self.som_pulo = pygame.mixer.Sound("sons/pulando.wav")
            self.som_pulo.set_volume(1)
            self.sprites = [] # cria uma lista
            self.sprites.append(pygame.image.load('imagens/meninocorrer1.png'))
            self.sprites.append(pygame.image.load('imagens/meninocorrer2.png'))
            self.sprites.append(pygame.image.load('imagens/meninocorrer3.png'))
            self.sprites.append(pygame.image.load('imagens/meninocorrer4.png')) # só pra colocar as sprites

            self.atual = 0 # pra comecar da primeira imagem
            self.image = self.sprites[self.atual] # pra mudar
            self.image = pygame.transform.scale(self.image, (32*13, 32*13)) 

            self.rect = self.image.get_rect() # pega tipo as cordenadas de onde tá a imagem 
            self.rect.topleft = largura-1400, altura-480 # pra dzr a posição onde o boneco vai ficar

            self.pos_y_inicial = altura-480 # pra dzr onde o boneco tá antes de pular
            self.pulo = False

        def pular(self):
            self.pulo = True 
            self.som_pulo.play()

        def update(self): # fzr update
                if self.pulo == True: # pra só se clicar no espaço acontecer as coisas 
                    if self.rect.y <= 100:
                        self.pulo = False
                    self.rect.y -= 100 # defie a posição q ele vai ficar na tela com o pulo
                else :
                    if self.rect.y < self.pos_y_inicial:
                        self.rect.y += 50  # pra o boneco descer
                    else :
                        self.rect.y = self.pos_y_inicial

                self.atual = self.atual + 0.5  # diminue a velocidade
                if self.atual >= len(self.sprites): # pra se repetir , no caso de quando acabar as sprits começa dnv
                    self.atual = 0  
                self.image = self.sprites[int(self.atual)] # é pra poder botar número quebrado
                self.image = pygame.transform.scale(self.image, (32*13, 32*13)) # aumenta o tamanho da img , a primeira é largura e a segunda é altura
        
        def morrer(self):
            tela.blit(pontuacao, (1300,30)) 
            tela.blit(gameover_img, gameover_rect)
            tela.blit(botao_reiniciar, botao_reiniciar_rect)
            tela.blit(botao_mapa, botao_mapa_rect)
           # pygame.display.update() # atualiza o jogo
           # pygame.time.delay(4000) #tem um delay antes de fechar a tela
           # pygame.quit() 
           # exit()



    todas_as_sprites = pygame.sprite.Group() # cria um grupo pra tds as sprites
    aluno = Aluno() # pra desenhar o aluno lá
    todas_as_sprites.add(aluno) # add aluno no grupo

    imagem_fundo = pygame.image.load("imagens/fundo_1.png").convert() # add a img de fundo
    imagem_fundo = pygame.transform.scale(imagem_fundo, (largura,altura)) # define o tamanho da img de fundo
    imagem_fundo_largura = imagem_fundo.get_width() # perguntar a mary (essas duas linhas servem pra ajustar o tamanho da imagem d fundo)
    tiles = math.ceil(largura / 700 ) #  perguntar a mary
    #rolagem lateral do fundo  e aumeto gradual da velocidade
    scroll = 0 
    velocidade_scroll = 100 #velocidade inicial da rolagem
    velocidade_maxima = 2000 
    aceleracao = 150 # o quanto a velocidade vai aumentar por segundo 

    relogio = pygame.time.Clock() # diz a velocidade
    estado = "jogando"
    while True:
        relogio.tick(20) # tempo
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() # é pra sair do jogo
                exit() # pra fechar a janela
            if event.type == KEYDOWN:
                if event.key == K_SPACE: # pra só acontecer quando apertar na tecla do espaço
                    if aluno.rect.y != aluno.pos_y_inicial: # pra n poder pular no ar
                        pass
                    else:
                        aluno.pular() # se ele tiver no chão aí pode pular

        for i in range (tiles):
            tela.blit(imagem_fundo, (i * imagem_fundo_largura + scroll, 0 ))

        # atualiza o fundo
        if estado == "jogando":
            if velocidade_scroll < velocidade_maxima:
                velocidade_scroll += aceleracao * dt
            elif velocidade_scroll > velocidade_maxima:
                velocidade_scroll = velocidade_maxima

            scroll -= velocidade_scroll * dt
                #reinicia o scroll mas não reseta a velocidade, se mantém a rolagem e a velocidade
            if abs(scroll) > imagem_fundo_largura:
                    scroll += imagem_fundo_largura

            todas_as_sprites.update() # faz o upgrade
            todas_as_sprites.draw(tela) # dsenha sapo na tela (q sapo mulher?)
            x -= velocidade_scroll * dt 
            if x <- cacto.get_width(): # coloca o cacto na rolagem tb 
                x = largura + 200
            cacto_rect.topleft = (x, y) # pega as posições do cacto
            tela.blit(cacto, cacto_rect) # desenha o cacto
            aluno_mask = pygame.mask.from_surface(aluno.image) # faz com que a colisão ocorra somente com os pixels visíveis, tanto do cacto como do aluno
            cacto_mask = pygame.mask.from_surface(cacto)

            offset = (cacto_rect.x - aluno.rect.x, cacto_rect.y - aluno.rect.y) # identifica a diferença das posições dos objetos na tela 
            if aluno_mask.overlap(cacto_mask, offset): # overlap verifica se existe colisão
                estado = "gameover"
            else:
                score += 100
                pontuacao = exibir_pontuacao(score, 50, (0,0,0))
            tela.blit(pontuacao, (1300,30)) 
        elif estado == "gameover":
            aluno.morrer()
            
        pygame.display.update() # processamennto 