import pyttsx3
import os
from datetime import datetime

class TTS:
    def __init__(self, voice_index: int = 1, rate: int = 150, volume: float = 1.0):
        self.voice_index = voice_index
        self.rate = rate
        self.volume = volume

    def speak(self, text: str):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[self.voice_index].id)
        engine.setProperty('rate', self.rate)
        engine.setProperty('volume', self.volume)
        engine.say(text)
        engine.runAndWait()
        # Không cần gọi stop()

    def save_to_wav(self, text: str, filename: str = None, save_dir: str = "saveaudio"):
        os.makedirs(save_dir, exist_ok=True)
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
        filepath = os.path.join(save_dir, filename)
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[self.voice_index].id)
        engine.setProperty('rate', self.rate)
        engine.setProperty('volume', self.volume)
        engine.save_to_file(text, filepath)
        engine.runAndWait()
        print(f"✅ Đã lưu giọng nói vào file: {filepath}")

if __name__ == "__main__":
    tts = TTS(voice_index=1, rate=150, volume=1.0)
    tts.speak("Xin chào! Tôi là trợ lý ảo của bạn.")
    tts.save_to_wav("Đây là một đoạn văn bản được chuyển thành giọng nói và lưu vào file.", filename="test_tts.wav")