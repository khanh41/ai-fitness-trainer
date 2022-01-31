import grpc

from app.core.constant import GRPC_URL
from app.core.utils import pillow_convert_base64
from app.grpc_services import infer_pb2_grpc, infer_pb2

_channel = grpc.insecure_channel(GRPC_URL)
_stub = infer_pb2_grpc.ExercisePredictStub(_channel)


def pose_predict_inference(exercise_name, image):
    image = image[:, :, ::-1]
    image = pillow_convert_base64(image)
    image = infer_pb2.ExercisePredictRequest(exercise_name=exercise_name, img_origin=image)

    # make the call
    response = _stub.Inference(image)
    return response.img_origin
