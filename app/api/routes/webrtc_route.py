import cv2
from aiortc import MediaStreamTrack
from aiortc.contrib.media import MediaPlayer, MediaRelay
from av.video import VideoFrame
from pydantic import BaseModel


class Offer(BaseModel):
    sdp: str
    type: str
    video_transform: str = None


class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, transform):
        super().__init__()
        self.track = track
        self.transform = transform

    async def recv(self):
        frame = await self.track.recv()

        if self.transform == "cartoon":
            img = frame.to_ndarray(format="bgr24")

            # prepare color
            img_color = cv2.pyrDown(cv2.pyrDown(img))
            for _ in range(6):
                img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
            img_color = cv2.pyrUp(cv2.pyrUp(img_color))

            # prepare edges
            img_edges = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            img_edges = cv2.adaptiveThreshold(
                cv2.medianBlur(img_edges, 7),
                255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY,
                9,
                2,
            )
            img_edges = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2RGB)

            # combine color and edges
            img = cv2.bitwise_and(img_color, img_edges)

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        elif self.transform == "edges":
            # perform edge detection
            img = frame.to_ndarray(format="bgr24")
            img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        elif self.transform == "rotate":
            # rotate image
            img = frame.to_ndarray(format="bgr24")
            rows, cols, _ = img.shape
            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), frame.time * 45, 1)
            img = cv2.warpAffine(img, M, (cols, rows))

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        # elif self.transform == "cv":
        #     img = frame.to_ndarray(format="bgr24")
        #     face = faces.detectMultiScale(img, 1.1, 19)
        #     for (x, y, w, h) in face:
        #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #
        #     eye = eyes.detectMultiScale(img, 1.1, 19)
        #     for (x, y, w, h) in eye:
        #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #
        #     # smile = smiles.detectMultiScale(img, 1.1, 19)
        #     # for (x, y, w, h) in smile:
        #     #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 5), 2)
        #
        #     new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        #     new_frame.pts = frame.pts
        #     new_frame.time_base = frame.time_base
        #     return new_frame
        else:
            return frame


def create_local_tracks(play_from=None):
    if play_from:
        player = MediaPlayer(play_from)
        return player.audio, player.video
    else:
        options = {"framerate": "30", "video_size": "1920x1080"}
        # if relay is None:
        # if platform.system() == "Darwin":
        # webcam = MediaPlayer(
        #     "default:none", format="avfoundation", options=options
        # )
        # elif platform.system() == "Windows":
        # webcam = MediaPlayer("video.mp4")
        webcam = MediaPlayer(
            "video=FULL HD 1080P Webcam", format="dshow", options=options
        )

        # else:
        # webcam = MediaPlayer("/dev/video0", format="v4l2", options=options)
        # audio, video = VideoTransformTrack(webcam.video, transform="cv")
        relay = MediaRelay()
        return None, relay.subscribe(webcam.video)
