from typing import List

from bson.objectid import ObjectId

from app.api.database.connect import exercise_trainer_collection
from app.api.helpers.convert_model2dict import exercise_trainer_helper


# Retrieve all exercise_trainers present in the database
def retrieve_exercise_trainers():
    exercise_trainers = []
    for exercise_trainer in exercise_trainer_collection.find():
        exercise_trainers.append(exercise_trainer_helper(exercise_trainer))
    return exercise_trainers


# Add a new exercise_trainer into to the database
def add_exercise_trainer(exercise_trainer_data: dict) -> dict:
    exercise_trainer = exercise_trainer_collection.insert_one(exercise_trainer_data)
    new_exercise_trainer = exercise_trainer_collection.find_one({"_id": exercise_trainer.inserted_id})
    return exercise_trainer_helper(new_exercise_trainer)


# Retrieve a exercise_trainer with a matching ID
def retrieve_exercise_trainer(id: str) -> dict:
    exercise_trainer = exercise_trainer_collection.find_one({"_id": ObjectId(id)})
    if exercise_trainer:
        return exercise_trainer_helper(exercise_trainer)


# Retrieve a exercise_trainer with a matching ID
def retrieves_exercise_trainer_by_race_id(id: str) -> List[dict]:
    exercise_trainers = []
    for exercise_trainer in exercise_trainer_collection.find({"raceID": id}):
        exercise_trainers.append(exercise_trainer_helper(exercise_trainer))
    return exercise_trainers


# Update a exercise_trainer with a matching ID
def update_exercise_trainer(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    exercise_trainer = exercise_trainer_collection.find_one({"_id": ObjectId(id)})
    if exercise_trainer:
        updated_exercise_trainer = exercise_trainer_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_exercise_trainer:
            return True
        return False


# Delete a exercise_trainer from the database
def delete_exercise_trainer(id: str):
    exercise_trainer = exercise_trainer_collection.find_one({"_id": ObjectId(id)})
    if exercise_trainer:
        exercise_trainer_collection.delete_one({"_id": ObjectId(id)})
        return True
