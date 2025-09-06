import os
from deepface import DeepFace
import cv2


class FaceRecognizer:
    """
    Lớp FaceRecognizer sử dụng DeepFace để:
    - Nhận diện danh tính khuôn mặt (face recognition)
    - Phát hiện khuôn mặt trong ảnh / camera
    """

    def __init__(self, db_path: str = "known_faces", model_name: str = "Facenet"):
        """
        :param db_path: Thư mục chứa ảnh khuôn mặt đã biết (DeepFace sẽ dùng để so sánh)
        :param model_name: Tên model backbone (VGG-Face, Facenet, ArcFace, Dlib, OpenFace…)
        """
        self.db_path = db_path
        self.model_name = model_name

        if not os.path.exists(db_path):
            os.makedirs(db_path)
            print(f"⚠️ Thư mục {db_path} chưa có, tạo mới...")

    def recognize_from_image(self, image_path: str):
        """
        Nhận diện khuôn mặt từ ảnh tĩnh
        :param image_path: đường dẫn ảnh
        :return: kết quả DeepFace.verify hoặc DeepFace.find
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Không tìm thấy ảnh: {image_path}")

        results = DeepFace.find(img_path=image_path,
                                db_path=self.db_path,
                                model_name=self.model_name,
                                enforce_detection=False)

        if len(results) > 0 and not results[0].empty:
            return results[0].to_dict(orient="records")  # Trả về danh sách khuôn mặt match
        else:
            return []

    def recognize_from_camera(self, camera_id: int = 0):
        """
        Nhận diện khuôn mặt trực tiếp từ webcam/camera
        Nhấn 'q' để thoát
        """
        cap = cv2.VideoCapture(camera_id)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            try:
                results = DeepFace.find(img_path=frame,
                                        db_path=self.db_path,
                                        model_name=self.model_name,
                                        enforce_detection=False)

                if len(results) > 0 and not results[0].empty:
                    identity = results[0].iloc[0]["identity"]
                    name = os.path.basename(identity).split(".")[0]
                else:
                    name = "Unknown"

                cv2.putText(frame, name, (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            except Exception as e:
                cv2.putText(frame, f"Lỗi: {str(e)}", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.imshow("DeepFace Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


# Test nhanh
if __name__ == "__main__":
    recog = FaceRecognizer(db_path="known_faces", model_name="Facenet")

    test_img = "test_face.jpg"
    if os.path.exists(test_img):
        results = recog.recognize_from_image(test_img)
        print("🔎 Kết quả:", results)
    else:
        print("⚠️ Không tìm thấy ảnh test")
