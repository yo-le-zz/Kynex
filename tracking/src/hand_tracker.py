from __future__ import annotations

import time
import urllib.request
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/"
    "hand_landmarker.task"
)


class HandTracker:
    def __init__(self, model_path: Path, camera_id: int = 0):
        self.model_path = model_path
        self.camera_id = camera_id

        self.cap: cv2.VideoCapture | None = None
        self.landmarker = None

    def ensure_model(self) -> None:
        if self.model_path.exists():
            return

        print("MediaPipe hand model not found.")
        print("Downloading model...")

        self.model_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            urllib.request.urlretrieve(
                MODEL_URL,
                self.model_path,
            )
        except Exception as exc:
            raise RuntimeError(
                f"Unable to download MediaPipe model: {exc}"
            ) from exc

        print("Model downloaded successfully.")

    def start(self) -> None:
        self.ensure_model()

        base_options = python.BaseOptions(
            model_asset_path=str(self.model_path)
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self.landmarker = vision.HandLandmarker.create_from_options(
            options
        )

        self.cap = cv2.VideoCapture(self.camera_id)

        if not self.cap.isOpened():
            raise RuntimeError(
                f"Unable to open webcam {self.camera_id}"
            )

        # Une résolution raisonnable évite de charger inutilement le CPU.
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def get_right_hand(self):
        if self.cap is None or self.landmarker is None:
            raise RuntimeError("HandTracker has not been started.")

        success, frame = self.cap.read()

        if not success:
            return None

        # MediaPipe travaille avec une image RGB.
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb,
        )

        timestamp_ms = int(time.monotonic() * 1000)

        result = self.landmarker.detect_for_video(
            mp_image,
            timestamp_ms,
        )

        if not result.hand_landmarks:
            return None

        # On cherche explicitement la main droite.
        for hand_index, handedness in enumerate(result.handedness):
            if not handedness:
                continue

            label = handedness[0].category_name

            if label.lower() == "right":
                return result.hand_landmarks[hand_index]

        return None

    def stop(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        if self.landmarker is not None:
            self.landmarker.close()
            self.landmarker = None