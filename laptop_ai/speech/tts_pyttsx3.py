import pyttsx3
import sounddevice as sd
import soundfile as sf
import os                          # Quản lý đường dẫn, thư mục
from datetime import datetime      # Tạo timestamp (thời gian hiện tại) cho tên file
import time

class TTS:
    def __init__(self, voice_index: int = 1, rate: int = 150, volume: float = 1.0):
        # Engine để nói
        self.engine_speak = pyttsx3.init()
        voices = self.engine_speak.getProperty('voices')
        self.engine_speak.setProperty('voice', voices[voice_index].id)
        self.engine_speak.setProperty('rate', rate)
        self.engine_speak.setProperty('volume', volume)

        # Engine để lưu file
        self.engine_save = pyttsx3.init()
        self.engine_save.setProperty('voice', voices[voice_index].id)
        self.engine_save.setProperty('rate', rate)
        self.engine_save.setProperty('volume', volume)

    def speak(self, text: str):
        self.engine_speak.say(text)
        self.engine_speak.runAndWait()

    def save_to_wav(self, text: str, filename: str = None, save_dir: str = "saveaudio"):
        os.makedirs(save_dir, exist_ok=True)
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
        filepath = os.path.join(save_dir, filename)
        self.engine_save.save_to_file(text, filepath)
        self.engine_save.runAndWait()
        print(f"✅ Đã lưu giọng nói vào file: {filepath}")


