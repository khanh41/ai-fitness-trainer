from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.api.database.execute.exercise_trainer import exercise_trainer_execute as execute
from app.api.database.models.exercise_trainer import ExerciseTrainerSchema
from app.api.responses.base import response
from app.logger.logger import configure_logging

logger = configure_logging(__name__)
router = APIRouter()


@router.post("/", response_description="exercise_trainer data added into the database")
async def add_exercise_trainer_data(exercise_trainer: ExerciseTrainerSchema = Body(...)):
    exercise_trainer = jsonable_encoder(exercise_trainer)
    execute.delete_data(exercise_trainer["exerciseId"])
    new_exercise_trainer = execute.add_data(exercise_trainer)
    response.base_response["data"] = new_exercise_trainer
    return response.base_response


@router.get("/search/{exercise_id}", response_description="exercise trainer data by name retrieved")
async def get_exercise_by_exercise_id(exercise_id):
    exercise = execute.retrieve_data_by_exercise_id(exercise_id)
    if exercise:
        response.base_response["data"] = exercise
        return response.base_response
    return response.error_response("A exercise doesn't exist.", 404)
