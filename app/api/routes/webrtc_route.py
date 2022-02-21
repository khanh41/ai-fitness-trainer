import cv2
from aiortc import MediaStreamTrack
from av.video import VideoFrame
from pydantic import BaseModel

from app.grpc_services import pose_predict_inference

relay = None
webcam = None


class Offer(BaseModel):
    sdp: str
    type: str
    video_transform: str = None


class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, exercise_name):
        super().__init__()
        self.track = track
        self.exercise_name = exercise_name

    async def recv(self):
        frame = await self.track.recv()
        img = frame.to_ndarray(format="bgr24")
        try:
            user_predict = pose_predict_inference("pushup1", "Push Up", img.copy())
        except:
            pass
        # rebuild a VideoFrame, preserving timing information
        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return frame
