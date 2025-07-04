import random

LABELS = ["person", "car", "animal", "crack", "defect", "none"]

def run_dummy_inference(frame):
    """
    Simulates AI model by returning a fake label and confidence score.
    """
    label = random.choice(LABELS)
    confidence = round(random.uniform(0.5, 0.99), 2)
    
    
    return {
        "label": label,
        "confidence": confidence
    }
