from app.api.database.cloud_storage import upload_file_google_storage
from app.core.utils import read_image_byte
from app.grpc_services import pose_predict_inference

def exercise_predict(image):
    image = image[:, :, ::-1]
    image = pillow_convert_base64(image)
    image = infer_pb2.ImgBase64(img_origin=image)

    # make the call
    response = stub.Inference(image)

    return response.img_origin

def save_image_to_firebase_storage(image, name: str):
    save_path = name.replace(" ", "").lower()
    upload_file_google_storage(image, save_path)
