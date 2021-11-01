from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.api.database.excute.user import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
)
from app.api.database.models.user import UserSchema
from app.api.responses.base import response
from app.logger.logger import configure_logging

logger = configure_logging(__name__)
router = APIRouter()


@router.post("/add", response_description="user data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = add_user(user)
    response.base_response["data"] = new_user
    return response.base_response


@router.get("/", response_description="users retrieved")
async def get_users():
    users = retrieve_users()
    if users:
        response.base_response["data"] = users
        return response.base_response
    return response.error_response("Empty list returned")


@router.get("/{id}", response_description="user data retrieved")
async def get_user_data(id):
    user = retrieve_user(id)
    if user:
        response.base_response["data"] = user
        return response.base_response
    return response.error_response("A user doesn't exist.", 404)


@router.put("/{id}")
async def update_user_data(id: str, req: UserSchema = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = update_user(id, req)
    if updated_user:
        return response.success_response(
            "user with ID: {} name update is successful".format(id),
        )
    return response.error_response(
        "There was an error updating the user data.",
        404,
    )


@router.delete("/{id}", response_description="user data deleted from the database")
async def delete_user_data(id: str):
    deleted_user = delete_user(id)
    if deleted_user:
        return response.success_response(
            "user with ID: {} removed".format(id), "user deleted successfully"
        )
    return response.error_response("user with id {0} doesn't exist".format(id), 404)
