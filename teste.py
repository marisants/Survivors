from vosk import Model, KaldiRecognizer
import pyaudio
import json

model = Model(r"C:\vosk\vosk-model-small-pt-0.3")
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()

stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=8000
)

stream.start_stream()
print("🎤 Pode falar (Ctrl+C para parar)")

try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            texto = result.get("text", "")
            if texto:
                print("Você disse:", texto)
except KeyboardInterrupt:
    print("\nEncerrando...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
