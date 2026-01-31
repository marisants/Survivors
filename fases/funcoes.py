import pygame
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import threading
import time

def tela_pause (tela, pontuacao):
    telap = pygame.image.load("ferramentas/img_pause2.png").convert_alpha()
    telap = pygame.transform.scale(telap, (950, 200))  # ajusta o tamanho
    telap_rect = telap.get_rect(center=(750, 200))

    fonte = pygame.font.Font("ferramentas/HVD_Comic_Serif_Pro.otf", 40)
    texto_info = fonte.render("Pressione ESC para continuar", True, (255, 255, 0))

    tela.blit(pontuacao, (1300,30))
    tela.blit(telap, telap_rect)
    tela.blit(texto_info, (445, 320))

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

