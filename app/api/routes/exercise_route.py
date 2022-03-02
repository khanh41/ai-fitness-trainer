from typing import List

from fastapi import APIRouter, Body, UploadFile, File
from fastapi.encoders import jsonable_encoder

from app.api.database.execute.exercise import exercise_execute as execute
from app.api.database.models.exercise import ExerciseSchema
from app.api.responses.base import response
from app.api.services import exercise_service
from app.logger.logger import configure_logging

logger = configure_logging(__name__)
router = APIRouter()


@router.post("/", response_description="exercise data added into the database")
async def add_exercise_data(exercise: ExerciseSchema = Body(...)):
    exercise = jsonable_encoder(exercise)
    new_exercise = execute.add_data(exercise)
    response.base_response["data"] = new_exercise
    return response.base_response


@router.post("/images", response_description="exercise images added")
async def add_exercise_images(name: str, files: List[UploadFile] = File(...)):
    for index, file in enumerate(files):
        content = await file.read()
        exercise_service.save_image_to_firebase_storage(content, name)
    return response.success_response()


@router.get("/", response_description="exercises retrieved")
async def get_exercises():
    exercises = execute.retrieve_datas()
    if exercises:
        response.base_response["data"] = exercises
        return response.base_response
    return response.error_response("Empty list returned")


@router.get("/{id}", response_description="exercise data retrieved")
async def get_exercise_data(id):
    exercise = execute.retrieve_data(id)
    if exercise:
        response.base_response["data"] = exercise
        return response.base_response
    return response.error_response("A exercise doesn't exist.", 404)


@router.put("/{id}")
async def update_exercise_data(id: str, req: ExerciseSchema = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_exercise = execute.update_data(id, req)
    if updated_exercise:
        return response.success_response(
            "exercise with ID: {} name update is successful".format(id),
        )
    return response.error_response(
        "There was an error updating the exercise data.",
        404,
    )


@router.delete("/{id}", response_description="exercise data deleted from the database")
async def delete_exercise_data(id: str):
    deleted_exercise = execute.delete_data(id)
    if deleted_exercise:
        return response.success_response(
            "exercise with ID: {} removed".format(id), "exercise deleted successfully"
        )
    return response.error_response("exercise with id {0} doesn't exist".format(id), 404)


@router.get("/search/{name}", response_description="exercise data by name retrieved")
async def get_exercise_by_name(name):
    exercise = execute.retrieve_data_by_name(name)
    if exercise:
        response.base_response["data"] = exercise
        return response.base_response
    return response.error_response("A exercise doesn't exist.", 404)


@router.post("/predict-form", response_description="exercise predicted")
async def predict_form(exercise_code: str, exercise_name: str, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        base64_img = exercise_service.exercise_predict(exercise_code, exercise_name, contents)
        response.base_response["data"] = base64_img
        return response.base_response
    except Exception as e:
        return response.error_response(str(e), 500)


@router.post("/predict-video", response_description="exercise predicted")
async def predict_video(exercise_name: str, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        data = exercise_service.exercise_predict_video(exercise_name, contents)
        response.base_response["data"] = data
        return response.base_response
    except Exception as e:
        return response.error_response(str(e), 500)


@router.post("/history-images", response_description="Exercise history images added")
async def add_exercise_images(files: List[UploadFile] = File(...)):
    for index, file in enumerate(files):
        content = await file.read()
        exercise_service.save_image_to_firebase_storage(content, "name")
    return response.success_response()
