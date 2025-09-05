import pyttsx3
import sounddevice as sd
import soundfile as sf

class TTS:
    #engine nó là đối tượng điều khiển giọng nói.Nếu không có engine, bạn không thể dùng bất kỳ chức năng nào của pyttsx3
    def __init__(self, voice_index: int = 1, rate: int = 150, volume: float = 1.0):
        self.engine = pyttsx3.init() #Khởi tạo engine của pyttsx3 – đây là bộ máy xử lý giọng nói. engine là đối tượng trung tâm để điều khiển giọng nói: nói, lưu file, chọn giọng...
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voice_index].id) #Lấy danh sách các giọng nói có sẵn trong hệ thống. 
        self.engine.setProperty('rate', rate) # Tốc độ nói
        self.engine.setProperty('volume', volume) # Âm lượng

    def speak(self, text: str):
        """Đọc văn bản bằng giọng nói"""
        self.engine.say(text) #đọc văn bản
        self.engine.runAndWait()#chạy và chờ cho đến khi tất cả các lệnh nói được hoàn thành

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
