import grpc

from app.core.constant import GRPC_URL
from app.grpc_services import infer_pb2_grpc

_channel = grpc.insecure_channel(GRPC_URL)

# create a stub (client)
stub = infer_pb2_grpc.ExercisePredictStub(_channel)
