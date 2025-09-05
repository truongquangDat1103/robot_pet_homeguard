import pyttsx3
import sounddevice as sd
import soundfile as sf

class TTS:
    def __init__(self, voice_index: int = 1, rate: int = 150, volume: float = 1.0):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voice_index].id)
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def speak(self, text: str):
        """Đọc văn bản bằng giọng nói"""
        self.engine.say(text)
        self.engine.runAndWait()

    def save_to_wav(self, text: str, filename: str = "output.wav"):
        """Lưu giọng nói thành file .wav"""
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()
        print(f"✅ Đã lưu giọng nói vào file: {filename}")

    def play_wav(self, filename: str):
        """Phát lại file .wav"""
        data, samplerate = sf.read(filename, dtype='float32')
        sd.play(data, samplerate)
        sd.wait()
