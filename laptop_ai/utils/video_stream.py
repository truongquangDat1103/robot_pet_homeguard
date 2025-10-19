import os
import threading
import time
from typing import Optional

import cv2
import requests


ESP32_STREAM_URL = os.environ.get("ESP32_STREAM_URL", "http://172.20.10.2:81/stream")
DASHBOARD_URL = os.environ.get("DASHBOARD_URL", "http://127.0.0.1:8000")


class VideoProcessor:
    def __init__(self,
                 esp32_url: str = ESP32_STREAM_URL,
                 dashboard_url: str = DASHBOARD_URL,
                 min_motion_area: int = 500):
        self.esp32_url = esp32_url
        self.dashboard_url = dashboard_url.rstrip("/")
        self.min_motion_area = min_motion_area
        self._stop = threading.Event()
        self._cap: Optional[cv2.VideoCapture] = None
        self._face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self._fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

    def stop(self):
        self._stop.set()

    def _open(self) -> bool:
        try:
            if self._cap is not None:
                self._cap.release()
            self._cap = cv2.VideoCapture(self.esp32_url)
            return self._cap.isOpened()
        except Exception:
            return False

    def _encode_jpeg(self, frame) -> Optional[bytes]:
        ok, buf = cv2.imencode('.jpg', frame)
        if not ok:
            return None
        return buf.tobytes()

    def _post(self, path: str, data: bytes):
        url = f"{self.dashboard_url}{path}"
        try:
            requests.post(url, data=data, headers={'Content-Type': 'image/jpeg'}, timeout=2)
        except Exception:
            pass

    def run(self):
        backoff = 1
        while not self._stop.is_set():
            if not self._open():
                time.sleep(backoff)
                backoff = min(10, backoff * 2)
                continue
            backoff = 1
            while not self._stop.is_set():
                ok, frame = self._cap.read()
                if not ok or frame is None:
                    break

                # Create face overlay
                face_frame = frame.copy()
                gray = cv2.cvtColor(face_frame, cv2.COLOR_BGR2GRAY)
                faces = self._face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))
                for (x, y, w, h) in faces:
                    cv2.rectangle(face_frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                    cv2.putText(face_frame, 'Face', (x, max(0, y-8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

                # Create motion overlay
                motion_frame = frame.copy()
                fgmask = self._fgbg.apply(motion_frame)
                blur = cv2.GaussianBlur(fgmask, (5, 5), 0)
                _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
                dilated = cv2.dilate(thresh, None, iterations=3)
                contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                motion = False
                for c in contours:
                    if cv2.contourArea(c) < self.min_motion_area:
                        continue
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(motion_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    motion = True
                if motion:
                    cv2.putText(motion_frame, 'Motion', (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

                # Encode and push
                f_jpg = self._encode_jpeg(face_frame)
                if f_jpg:
                    self._post('/ingest/face', f_jpg)
                m_jpg = self._encode_jpeg(motion_frame)
                if m_jpg:
                    self._post('/ingest/motion', m_jpg)

        # cleanup
        try:
            if self._cap is not None:
                self._cap.release()
        except Exception:
            pass


def start_in_background() -> VideoProcessor:
    proc = VideoProcessor()
    t = threading.Thread(target=proc.run, daemon=True)
    t.start()
    return proc
