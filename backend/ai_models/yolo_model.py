from ultralytics import YOLO

model = YOLO("yolov5s.pt")  

def run_yolo_inference(frame):
    """
    Runs YOLOv5 on a single image frame.
    Returns list of detections: label, confidence, box.
    """
    results = model.predict(source=frame, imgsz=640, conf=0.5, verbose=False)
    
    detections = []
    for r in results:
        for box in r.boxes:
            label = r.names[int(box.cls[0])]
            confidence = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()

            detections.append({
                "label": label,
                "confidence": round(confidence, 2),
                "box": [round(x, 2) for x in xyxy]
            })

    return detections
