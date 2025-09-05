# ...existing code...
from model.qwen_ai import Qwen3Chat
from speech.stt_whisper import PhoWhisperSTT
from speech.tts_pyttsx3 import TTS
from audio.recorder import Recorder
from speech.voice_assistant import VoiceAssistant
if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()