# ...existing code...
from model.qwen_ai import Qwen3Chat
from speech.stt_whisper import PhoWhisperSTT
from speech.tts_pyttsx3 import TTS
from audio.recorder import Recorder

def main():
    print("Khởi động Robot Pet HomeGuard AI!")
    # Khởi tạo các module
    ai_chat = Qwen3Chat()
    stt = PhoWhisperSTT()
    tts = TTS()
    recorder = Recorder()

    # Ghi âm và nhận diện giọng nói
    print("Thu âm lệnh từ người dùng...")
    audio_file = recorder.record(duration=5)
    user_text = stt.transcribe(audio_file)
    print(f"Bạn nói: {user_text}")

    # Chat với AI
    ai_reply = ai_chat.ask(user_text)
    print(f"🤖 AI trả lời: {ai_reply}")

    # Đọc lại câu trả lời bằng giọng nói
    tts.speak(ai_reply)
    tts.save_to_wav(ai_reply, "ai_response.wav")

if __name__ == "__main__":
    main()
# ...existing code...