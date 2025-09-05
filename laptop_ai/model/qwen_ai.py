import ollama

class Qwen3Chat:
    #hàm khởi tạo constructer 
    def __init__(self, model="qwen3:8b", system_prompt="Bạn là một Robot thú cưng trông nhà."):
        self.model = model
        self.system_prompt = system_prompt
        self.history = [
            {"role": "system", "content": self.system_prompt} #khởi tạo vai trò của ai
        ]

    def ask(self, user_input: str) -> str:
        """
        Gửi câu hỏi của user tới Qwen3 và nhận câu trả lời
        """
        # Thêm message của user vào lịch sử
        self.history.append({"role": "user", "content": user_input})

        try:
            # Gọi API Ollama để chat với Qwen3
            response = ollama.chat(
                model=self.model,
                messages=self.history,
                think=False
            )

            # Lấy content trả lời
            ai_reply = response['message']['content']

            # Lưu lại vào lịch sử hội thoại
            self.history.append({"role": "assistant", "content": ai_reply})

            return ai_reply
        #xử lý ngoại lệ    
        except Exception as e:
            return f"Lỗi khi gọi Qwen3: {e}"

    def reset(self):
        """Reset hội thoại về trạng thái ban đầu"""
        self.history = [
            {"role": "system", "content": self.system_prompt}
        ]


# Test nhanh khi chạy trực tiếp file này
if __name__ == "__main__":
    bot = Qwen3Chat()
    reply = bot.ask("Xin chào, bạn có thể làm gì?")
    print("🤖:", reply)
