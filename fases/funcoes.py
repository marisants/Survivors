import pygame
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import threading
import time
import math

def tela_pause (tela, pontuacao):
    telap = pygame.image.load("ferramentas/img_pause2.png").convert_alpha()
    telap = pygame.transform.scale(telap, (950, 200))  # ajusta o tamanho
    telap_rect = telap.get_rect(center=(750, 200))

    fonte = pygame.font.Font("ferramentas/HVD_Comic_Serif_Pro.otf", 40)
    texto_info = fonte.render("Pressione ESC para continuar", True, (255, 255, 0))

    tela.blit(pontuacao, (1300,30))
    tela.blit(telap, telap_rect)
    tela.blit(texto_info, (445, 320))

def ultima_tela(tela, largura, altura):
    clock = pygame.time.Clock()

    imagem_fundo = pygame.image.load("ferramentas/img_fim.png").convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))

    # TEXTO FIM
    texto_fim = pygame.image.load("ferramentas/texto_fim.png").convert_alpha()
    texto_fim = pygame.transform.scale(texto_fim, (800, 180))
    texto_fim_rect = texto_fim.get_rect(topleft=(250, 60))

    # TEXTO V
    texto_v = pygame.image.load("ferramentas/texto_v.png").convert_alpha()
    texto_v = pygame.transform.scale(texto_v, (650, 160))
    texto_v_rect = texto_v.get_rect(topleft=(250, 260))

    # BOTÃO MENOR E ALINHADO COM OS TEXTOS
    botao_reiniciar = pygame.image.load("ferramentas/reiniciar_a.png").convert_alpha()
    botao_reiniciar = pygame.transform.scale(botao_reiniciar, (220, 100))

    botao_reiniciar_rect = botao_reiniciar.get_rect(
        centerx=texto_fim_rect.centerx,
        top=texto_v_rect.bottom + 40
    )

    rodando = True
    while rodando:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_reiniciar_rect.collidepoint(event.pos):
                    return "FASE_1"


        tela.blit(imagem_fundo, (0, 0))
        tela.blit(texto_fim, texto_fim_rect)
        tela.blit(texto_v, texto_v_rect)
        tela.blit(botao_reiniciar, botao_reiniciar_rect)

        pygame.display.update()


    
def tela_vitoria (tela, pontuacao):
    telav = pygame.image.load("ferramentas/img_vitoria.png").convert_alpha()
    telav = pygame.transform.scale(telav, (950, 200))  # ajusta o tamanho
    telav_rect = telav.get_rect(center=(750, 200))

    botao_reiniciar = pygame.image.load("ferramentas/reiniciar_v.png").convert_alpha()
    botao_reiniciar = pygame.transform.scale(botao_reiniciar, (400, 100))  # ajusta o tamanho
    botao_reiniciar_rect = botao_reiniciar.get_rect(center=(750, 390))

    botao_proximo = pygame.image.load("ferramentas/botao_proximo.png").convert_alpha()
    botao_proximo = pygame.transform.scale(botao_proximo, (400, 100))  # ajusta o tamanho
    botao_proximo_rect = botao_proximo.get_rect(center=(750, 510))

    tela.blit(pontuacao, (1300, 30))
    tela.blit(telav, telav_rect)
    tela.blit(botao_reiniciar, botao_reiniciar_rect)
    tela.blit(botao_proximo, botao_proximo_rect)
    
#comando de voz 
comando_voz = None

model = Model("C:/vosk/vosk-model-small-pt-0.3")
rec = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=4096
)
stream.start_stream()

def ouvir_voz():
    global comando_voz
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            resultado = json.loads(rec.Result())
            texto = resultado.get("text", "").lower().strip()
            if texto:
                print("VOZ:", texto)
                comando_voz = texto

threading.Thread(target=ouvir_voz, daemon=True).start()

