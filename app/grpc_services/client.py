import grpc
from cv2 import cv2

from app.core.utils import pillow_convert_base64
from app.grpc_services import infer_pb2, infer_pb2_grpc

channel = grpc.insecure_channel('2.tcp.ngrok.io:16976')

# create a stub (client)
stub = infer_pb2_grpc.ExercisePredictStub(channel)

# create a valid request message
img = cv2.imread("test_pose.jpg")
img = img[:, :, ::-1]
img = pillow_convert_base64(img)
number = infer_pb2.ImgBase64(img_origin=img)

# make the call
response = stub.Inference(number)

print(response.img_origin)
