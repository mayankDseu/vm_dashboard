import random

def classify_bolt(cropped_image):
    """
    Simulated bolt classifier.
    Replace this with a real PyTorch/TensorFlow model later.
    """
    labels = ["OK", "DEFECT", "RUSTY", "MISSING_HEAD"]
    return {
        "class": random.choice(labels),
        "confidence": round(random.uniform(0.6, 0.99), 2)
    }
