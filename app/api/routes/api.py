from fastapi import APIRouter

from app.api.routes import user_route, exercise_route

app = APIRouter()
app.include_router(user_route.router, tags=["Name Card Detection"], prefix="/name-card-detection")
app.include_router(exercise_route.router, tags=["Name Card Detection"], prefix="/name-card-detection")
