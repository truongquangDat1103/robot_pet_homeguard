import cv2
import face_recognition

# Tải ảnh mẫu
known_image = face_recognition.load_image_file("person.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# Mở webcam
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Chuyển sang RGB (OpenCV đọc BGR)
    rgb_frame = frame[:, :, ::-1]

    # Phát hiện khuôn mặt
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # So sánh khuôn mặt
        matches = face_recognition.compare_faces([known_encoding], face_encoding)

        name = "Người lạ"
        if matches[0]:
            name = "Đã biết"

        # Vẽ khung + label
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    cv2.imshow("Nhận diện khuôn mặt", frame)

    # Bấm Q để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
