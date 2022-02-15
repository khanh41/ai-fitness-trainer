import os

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from app.core.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from app.api.database.migrate.init_super_user import init_super_user
from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.core.constant import AiPredict

HOST = os.getenv("APP_HOST")
PORT = os.getenv("APP_PORT")
CHUNK_SIZE = 1024 * 1024


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

    # templates = Jinja2Templates(directory="app/frontend/templates")

    # @application.get("/", tags=["UI"], response_class=HTMLResponse, include_in_schema=False)
    # async def read_root(request: Request):
    #     return templates.TemplateResponse("index.html", {"request": request})

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
