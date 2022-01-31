from app.api.database.cloud_storage import upload_file_google_storage
from app.core.utils import read_image_byte
from app.grpc_services import pose_predict_inference


def exercise_predict(exercise_name, user_image):
    user_image = read_image_byte(user_image)
    user_predict = pose_predict_inference(exercise_name, user_image)
    return user_predict


def save_image_to_firebase_storage(image, name: str):
    save_path = name.replace(" ", "").lower()
    upload_file_google_storage(image, save_path)
