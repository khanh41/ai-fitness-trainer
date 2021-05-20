import os
from pathlib import Path

from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, StreamingResponse

from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.core.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, PROJECT_NAME, VERSION

HOST = os.getenv("APP_HOST")
PORT = os.getenv("APP_PORT")
CHUNK_SIZE = 1024 * 1024
video_path = Path("video.mp4")


def get_application() -> FastAPI:
    from app.api.routes.api import app as api_router

    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
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

    application.mount(
        "/static", StaticFiles(directory="app/frontend/static"), name="static"
    )
    templates = Jinja2Templates(directory="app/frontend/templates")

    @application.get("/", tags=["UI"], response_class=HTMLResponse, include_in_schema=False)
    async def read_root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @application.get("/video")
    async def video_endpoint():
        def iterfile():
            with open(video_path, mode="rb") as file_like:
                yield from file_like

        return StreamingResponse(iterfile(), media_type="video/mp4")

    return application


app = get_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=int(PORT))
