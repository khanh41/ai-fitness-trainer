import grpc

from app.core.utils import pillow_convert_base64
from app.grpc_services import infer_pb2, infer_pb2_grpc

channel = grpc.insecure_channel('2.tcp.ngrok.io:16976')

# create a stub (client)
stub = infer_pb2_grpc.ExercisePredictStub(channel)


def exercise_predict(image):
    image = image[:, :, ::-1]
    image = pillow_convert_base64(image)
    image = infer_pb2.ImgBase64(img_origin=image)

    # make the call
    response = stub.Inference(image)

    return response.img_origin
