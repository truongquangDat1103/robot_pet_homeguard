import os
import cv2
from deepface import DeepFace
import numpy as np


class FaceRecognizer:
    def __init__(self, db_path="known_faces", model_name="Facenet"):
        self.db_path = db_path
        self.model_name = model_name
        self.embeddings = []

        if not os.path.exists(db_path):
            os.makedirs(db_path)
            print(f"⚠️ Thư mục {db_path} chưa có, tạo mới...")

        self._load_known_faces() #chạy hàm tạo embeding

    def _load_known_faces(self):
        """Tạo embedding cho tất cả ảnh trong db"""
        for file in os.listdir(self.db_path):
            path = os.path.join(self.db_path, file) #join dùng để nối các phần của đường dẫn lại với nhau, sau khi nối thì path sẽ có  đường dẫn đầy đủ
            if os.path.isfile(path):                 #kiểm tra xem path có phải là file không, chỉ xử lý file, bỏ qua thư mục con
                try:
                    rep = DeepFace.represent(img_path=path, model_name=self.model_name, enforce_detection=False) #tạo embedding cho ảnh
                    self.embeddings.append({                # thêm embedding vào danh sách, append là thêm phần tử vào cuối danh sách   
                        "name": os.path.splitext(file)[0],   # tên file (bỏ đuôi) làm nhãn
                        "embedding": rep[0]["embedding"]     # vector 128D/512D (tuỳ model)
                    })
                except Exception as e:
                    print(f"Lỗi khi load {file}: {e}")

    def _cosine_similarity(self, emb1, emb2):   #Hàm này nhận vào hai vector emb1 và emb2 (đại diện cho hai khuôn mặt),
        emb1, emb2 = np.array(emb1), np.array(emb2) #Chuyển đổi emb1 và emb2 từ kiểu list sang kiểu NumPy array
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)) #tích vô hướng của hai vector chia cho tích của độ dài (norm) của chúng, Kết quả nằm trong khoảng từ -1 đến 1, càng gần 1 thì hai khuôn mặt càng giống nhau.

    def recognize_from_camera(self, camera_id=0, threshold=0.7):
        cap = cv2.VideoCapture(camera_id)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            try:
                # Tạo embedding cho frame hiện tại
                rep = DeepFace.represent(frame, model_name=self.model_name, enforce_detection=False)

                if rep:
                    face_emb = rep[0]["embedding"]
                    best_match, best_score = "Unknown", 0

                    for item in self.embeddings:
                        score = self._cosine_similarity(face_emb, item["embedding"])
                        if score > best_score:
                            best_match, best_score = item["name"], score

                    if best_score >= threshold:
                        name = best_match
                    else:
                        name = "Unknown"
                else:
                    name = "No face"

                cv2.putText(frame, name, (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            except Exception as e:
                cv2.putText(frame, f"Lỗi: {str(e)}", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.imshow("Face Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
