from app.ml.data_loader import load_image
from app.ml.trainers.push_up import PushUpTrainer

trainer = PushUpTrainer()

image = load_image("C:\\Users\\tranv\Downloads\\FEATURE1-1200x628.jpg")
trainer.predict(image)
