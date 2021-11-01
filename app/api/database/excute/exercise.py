from typing import List

from bson.objectid import ObjectId

from app.api.database.connect import exercise_collection
from app.api.helpers.convert_model2dict import exercise_helper


# Retrieve all exercises present in the database
def retrieve_exercises():
    exercises = []
    for exercise in exercise_collection.find():
        exercises.append(exercise_helper(exercise))
    return exercises


# Add a new exercise into to the database
def add_exercise(exercise_data: dict) -> dict:
    exercise = exercise_collection.insert_one(exercise_data)
    new_exercise = exercise_collection.find_one({"_id": exercise.inserted_id})
    return exercise_helper(new_exercise)


# Retrieve a exercise with a matching ID
def retrieve_exercise(id: str) -> dict:
    exercise = exercise_collection.find_one({"_id": ObjectId(id)})
    if exercise:
        return exercise_helper(exercise)


# Retrieve a exercise with a matching ID
def retrieves_exercise_by_race_id(id: str) -> List[dict]:
    exercises = []
    for exercise in exercise_collection.find({"raceID": id}):
        exercises.append(exercise_helper(exercise))
    return exercises


# Update a exercise with a matching ID
def update_exercise(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    exercise = exercise_collection.find_one({"_id": ObjectId(id)})
    if exercise:
        updated_exercise = exercise_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_exercise:
            return True
        return False


# Delete a exercise from the database
def delete_exercise(id: str):
    exercise = exercise_collection.find_one({"_id": ObjectId(id)})
    if exercise:
        exercise_collection.delete_one({"_id": ObjectId(id)})
        return True
