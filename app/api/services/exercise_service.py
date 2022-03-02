import uuid

from app.api.database.cloud_storage import upload_file_google_storage
from app.core.constant import AiPredict
from app.core.utils import read_image_byte, save_byte_to_video
from app.grpc_services import pose_predict_inference, pose_predict_video_inference


def exercise_predict(exercise_code, exercise_name, user_image):
    user_image = read_image_byte(user_image)
    user_predict = pose_predict_inference(exercise_code, exercise_name, user_image)

    image_name = str(uuid.uuid4()) + ".jpg"
    save_image_to_firebase_storage(user_predict, image_name)

    return user_predict


def exercise_predict_video(exercise_name, user_video):
    user_video_id = save_byte_to_video(user_video)
    user_predict = pose_predict_video_inference(exercise_name, user_video_id)

    AiPredict.predict_video_path, predict_video_id = user_predict.split('split--character')
    return predict_video_id[:-4]


def save_image_to_firebase_storage(image, name: str):
    save_path = name.replace(" ", "").lower()
    upload_file_google_storage(image, save_path)

