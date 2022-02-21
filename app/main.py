import asyncio
import os

from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaRelay, MediaBlackhole
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from app.api.database.migrate.init_super_user import init_super_user
from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.api.routes.webrtc_route import VideoTransformTrack, Offer, create_local_tracks
from app.core.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from app.core.constant import AiPredict

HOST = os.getenv("APP_HOST")
PORT = os.getenv("APP_PORT")


def get_application() -> FastAPI:
    from app.api.routes.api import app as api_router
    from app.api.routes import authentication

    init_super_user()

    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION, docs_url=None)
    print()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # application.add_event_handler("startup", create_start_app_handler(application))
    # application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=API_PREFIX)
    application.include_router(authentication.router, tags=["Authentication"])

    application.mount(
        "/static", StaticFiles(directory="app/frontend/static"), name="static"
    )

    templates = Jinja2Templates(directory="app/frontend/templates")

    @application.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @application.get("/cv", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index_cv.html", {"request": request})

    @application.post("/offer")
    async def offer(params: Offer):
        offer = RTCSessionDescription(sdp=params.sdp, type=params.type)

        pc = RTCPeerConnection()
        pcs.add(pc)
        recorder = MediaBlackhole()

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            print("Connection state is %s" % pc.connectionState)
            if pc.connectionState == "failed":
                await pc.close()
                pcs.discard(pc)

        # open media source
        audio, video = create_local_tracks()

        # handle offer
        await pc.setRemoteDescription(offer)
        await recorder.start()

        # send answer
        answer = await pc.createAnswer()

        await pc.setRemoteDescription(offer)
        for t in pc.getTransceivers():
            if t.kind == "audio" and audio:
                pc.addTrack(audio)
            elif t.kind == "video" and video:
                pc.addTrack(video)

        await pc.setLocalDescription(answer)

        return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}

    @application.post("/offer_cv")
    async def offer(params: Offer):
        offer = RTCSessionDescription(sdp=params.sdp, type=params.type)

        pc = RTCPeerConnection()
        pcs.add(pc)
        recorder = MediaBlackhole()

        relay = MediaRelay()

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            print("Connection state is %s" % pc.connectionState)
            if pc.connectionState == "failed":
                await pc.close()
                pcs.discard(pc)

        # open media source
        # audio, video = create_local_tracks()

        @pc.on("track")
        def on_track(track):

            # if track.kind == "audio":
            #     pc.addTrack(player.audio)
            #     recorder.addTrack(track)
            if track.kind == "video":
                pc.addTrack(
                    VideoTransformTrack(relay.subscribe(track), transform=params.video_transform)
                )
                # if args.record_to:
                #     recorder.addTrack(relay.subscribe(track))

            @track.on("ended")
            async def on_ended():
                await recorder.stop()

        # handle offer
        await pc.setRemoteDescription(offer)
        await recorder.start()

        # send answer
        answer = await pc.createAnswer()
        await pc.setRemoteDescription(offer)
        await pc.setLocalDescription(answer)

        return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}

    pcs = set()
    args = ''

    @application.on_event("shutdown")
    async def on_shutdown():
        # close peer connections
        coros = [pc.close() for pc in pcs]
        await asyncio.gather(*coros)
        pcs.clear()

    @application.get("/video/{video_id}")
    async def video_endpoint(video_id):
        def iterfile():
            with open(os.path.join(AiPredict.predict_video_path,
                                   video_id + '.mp4'), mode="rb") as file_like:
                yield from file_like

        return StreamingResponse(iterfile(), media_type="video/mp4")

    return application


app = get_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=int(PORT))
