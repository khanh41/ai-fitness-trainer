from fastapi import APIRouter

from app.api.routes import user_route, exercise_route

app = APIRouter()

app.include_router(user_route.router, tags=["User"], prefix="/admin/user")
app.include_router(exercise_route.router, tags=["Exercise"], prefix="/admin/exercise")
