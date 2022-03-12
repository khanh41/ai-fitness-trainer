import grpc

from app.core.constant import GRPC_URL
from app.core.utils import pillow_convert_base64
from app.grpc_services import infer_pb2_grpc, infer_pb2

_channel = grpc.insecure_channel(GRPC_URL)
_image_inference_stub = infer_pb2_grpc.ExerciseImagePredictStub(_channel)
_video_inference_stub = infer_pb2_grpc.ExerciseVideoPredictStub(_channel)
_update_config_stub = infer_pb2_grpc.UpdateDataConfigStub(_channel)


def pose_predict_inference(exercise_code, exercise_name, image):
    image = image[:, :, ::-1]
    image = pillow_convert_base64(image)
    data = infer_pb2.Param3Request(param_1=exercise_code,
                                   param_2=exercise_name,
                                   param_3=image)

    # make the call
    response = _image_inference_stub.ImageInference(data)
    return response.param_1, response.param_2


def pose_predict_video_inference(exercise_name, video_path):
    data = infer_pb2.Param2Request(param_1=exercise_name,
                                   param_2=video_path)

    # make the call
    response = _video_inference_stub.VideoInference(data)
    return response.param_1


def update_config():
    image = infer_pb2.Param1Request(temp='')

    # make the call
    response = _update_config_stub.UpdateConfig(image)
    return response.param_1
