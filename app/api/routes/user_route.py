from fastapi import APIRouter, Body
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.api.database.execute.user import user_execute as execute
from app.api.database.execute.user_information import user_information_execute
from app.api.database.models.user import UserSchema
from app.api.database.models.user_information import UserInformationSchema
from app.api.responses.base import response
from app.api.services import authentication_service
from app.logger.logger import configure_logging

logger = configure_logging(__name__)
router = APIRouter()


@router.post("/", response_description="user data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    exist_username = execute.retrieve_data_by_username(user['username'])
    if exist_username:
        return response.error_response("Username exist")

    user['password'] = authentication_service.get_password_hash(user['password'])
    new_user = execute.add_data(user)
    response.base_response["data"] = new_user

    user_infor_data = UserInformationSchema.Config.schema_extra['example']
    user_infor_data['userId'] = new_user['id']
    user_infor_data['email'] = new_user['username']
    user_information_execute.add_data(user_infor_data)

    return response.base_response


@router.get("/", response_description="users retrieved")
async def get_users():
    users = execute.retrieve_datas()
    if users:
        response.base_response["data"] = users
        return response.base_response
    return response.error_response("Empty list returned")


@router.get("/{id}", response_description="user data retrieved")
async def get_user_data(id):
    user = execute.retrieve_data(id)
    if user:
        response.base_response["data"] = user
        return response.base_response
    return response.error_response("A user doesn't exist.", 404)


@router.put("/{id}")
async def update_user_data(id: str, req: UserSchema = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = execute.update_data(id, req)
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
    deleted_user = execute.delete_data(id)
    if deleted_user:
        return response.success_response("user with ID: {} removed".format(id))
    return response.error_response("user with id {0} doesn't exist".format(id), 404)


@router.get("/me/image-history")
async def get_image_history(current_user: UserSchema = Depends(authentication_service.get_current_active_user)):
    user_data = execute.retrieve_data_by_username(current_user['username'])
    user_data = user_information_execute.retrieve_data_by_user_id(user_data['id'])
    response.base_response["data"] = user_data['historyImages']
    return response.base_response


@router.post("/me/image-history/{image_name}")
async def add_image_history(image_name: str,
                            current_user: UserSchema = Depends(authentication_service.get_current_active_user)):
    if image_name:
        user_data = execute.retrieve_data_by_username(current_user['username'])
        user_data = user_information_execute.retrieve_data_by_user_id(user_data['id'])
        user_data['historyImages'].insert(0, image_name)

        _id = user_data.pop('id')
        user_information_execute.update_data(_id, user_data)

        return response.success_response()
    return response.error_response()
