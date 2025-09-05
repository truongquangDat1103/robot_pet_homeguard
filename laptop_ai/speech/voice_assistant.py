from model.qwen_ai import Qwen3Chat
from speech.stt_whisper import PhoWhisperSTT
from speech.tts_pyttsx3 import TTS
from audio.recorder import Recorder

class VoiceAssistant:
    def __init__(self):
        print("Khởi tạo VoiceAssistant...")
        self.ai_chat = Qwen3Chat()
        self.stt = PhoWhisperSTT()
        self.tts = TTS()
        self.recorder = Recorder()

    def run(self):
        print("Khởi động Robot Pet HomeGuard AI!")
        print("Thu âm lệnh từ người dùng...")
        audio_file = self.recorder.record(duration=5)
        user_text = self.stt.transcribe(audio_file)
        print(f"Bạn nói: {user_text}")

        ai_reply = self.ai_chat.ask(user_text)
        print(f"🤖 AI trả lời: {ai_reply}")

        self.tts.speak(ai_reply)
        #self.tts.save_to_wav(ai_reply, "ai_response.wav")
