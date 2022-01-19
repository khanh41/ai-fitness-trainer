from app.core.utils import pillow_convert_base64
from app.grpc_services import infer_pb2, stub


def exercise_predict(image):
    image = image[:, :, ::-1]
    image = pillow_convert_base64(image)
    image = infer_pb2.ImgBase64(img_origin=image)

    # make the call
    response = stub.Inference(image)

    return response.img_origin


def save_image_to_firebase_storage(image):
    pass
