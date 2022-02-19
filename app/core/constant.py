import os
from pathlib import Path

GRPC_URL = os.getenv("GRPC_URL")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
FIREBASE_IMAGE_URL = lambda x: f"https://firebasestorage.googleapis.com/v0/b/aift-b7b2c.appspot.com/o/{x}.jpg?alt=media"

VIDEO_PATH = "app/resources/videos"

MONGO_DETAILS = os.getenv("MONGO_DETAILS")
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ADMIN_USER = -1
SUPER_USERNAME = os.getenv('SUPER_USERNAME')
SUPER_PASSWORD = os.getenv('SUPER_PASSWORD')

ROOT_PATH = Path(__file__).parent.parent.parent


class AiPredict:
    predict_video_path = ''
