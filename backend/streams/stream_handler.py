import cv2
import threading
import os
import time

from ai_models.yolo_model import run_yolo_inference
from ai_models.classifier_model import classify_bolt

class VideoStreamHandler:
    def __init__(self, stream_id, source_path, output_dir="outputs"):
        self.predictions = []
        self.stream_id = stream_id
        self.source_path = source_path
        self.output_dir = os.path.join(output_dir, f"stream_{stream_id}")
        self.capture = None
        self.running = False
        self.thread = None

        os.makedirs(self.output_dir, exist_ok=True)
        print(f"[Stream {self.stream_id}] Output directory: {self.output_dir}")

    def start(self):
        if self.running:
            print(f"[Stream {self.stream_id}] Already running.")
            return

        self.capture = cv2.VideoCapture(self.source_path)
        if not self.capture.isOpened():
            print(f"[Stream {self.stream_id}] ❌ Failed to open: {self.source_path}")
            return

        self.running = True
        self.thread = threading.Thread(target=self._process_stream, daemon=True)
        self.thread.start()
        print(f"[Stream {self.stream_id}] ✅ Started.")

    def stop(self):
        self.running = False
        if self.capture:
            self.capture.release()
            print(f"[Stream {self.stream_id}] 🔴 Stopped.")

    def _process_stream(self):
        frame_count = 0
        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                print(f"[Stream {self.stream_id}] ⚠️ Read failed or end of stream.")
                break

            print(f"[Stream {self.stream_id}] Read frame {frame_count}")

            if frame is None or not hasattr(frame, "shape"):
                print(f"[Stream {self.stream_id}] ❌ Invalid frame (None or no shape)")
                continue

            # Save every 30th frame
            if frame_count % 30 == 0:
                filename = os.path.join(self.output_dir, f"frame_{frame_count}.jpg")
                success = cv2.imwrite(filename, frame)
                if success:
                    print(f"[Stream {self.stream_id}] ✅ Saved: {filename}")

                    
                    detections = run_yolo_inference(frame)
                    classified_results = []

                    for detection in detections:
                        x1, y1, x2, y2 = map(int, detection['box'])
                        cropped = frame[y1:y2, x1:x2]

                        
                        classification = classify_bolt(cropped)

                        classified_results.append({
                            "detection": detection,
                            "classification": classification
                        })

                    print(f"[Stream {self.stream_id}] 🧠 Final Results: {classified_results}")
                    self.predictions.append({
                        "frame": frame_count,
                        "results": classified_results
                    })
                else:
                    print(f"[Stream {self.stream_id}] ❌ Failed to save: {filename}")

            frame_count += 1
            time.sleep(1 / 30)  

        self.capture.release()
        print(f"[Stream {self.stream_id}] 🛑 Processing complete.")
