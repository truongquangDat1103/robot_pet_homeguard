from tts_pyttsx3 import TTS  # nếu bạn lưu class TTS trong file TTS.py

def main():
    # Khởi tạo đối tượng TTS với giọng đầu tiên
    tts = TTS(voice_index=1, rate=150, volume=1.0)

    # Văn bản cần chuyển thành giọng nói
    text = "Xin chào, tôi là robot thú cưng trông nhà. Tôi có thể phát hiện chuyển động và nhận diện người lạ."

    # Lưu giọng nói vào file .wav
    tts.save_to_wav(text, filename="robot_voice.wav")

    # Phát lại file vừa lưu
    tts.play_wav("robot_voice.wav")

if __name__ == "__main__":
    main()
