from typing import List

from bson.objectid import ObjectId

from app.api.database.connect import user_exercise_collection
from app.api.helpers.convert_model2dict import user_exercise_helper


# Retrieve all user_exercises present in the database
def retrieve_user_exercises():
    user_exercises = []
    for user_exercise in user_exercise_collection.find():
        user_exercises.append(user_exercise_helper(user_exercise))
    return user_exercises


# Add a new user_exercise into to the database
def add_user_exercise(user_exercise_data: dict) -> dict:
    user_exercise = user_exercise_collection.insert_one(user_exercise_data)
    new_user_exercise = user_exercise_collection.find_one({"_id": user_exercise.inserted_id})
    return user_exercise_helper(new_user_exercise)


# Retrieve a user_exercise with a matching ID
def retrieve_user_exercise(id: str) -> dict:
    user_exercise = user_exercise_collection.find_one({"_id": ObjectId(id)})
    if user_exercise:
        return user_exercise_helper(user_exercise)


# Retrieve a user_exercise with a matching ID
def retrieves_user_exercise_by_race_id(id: str) -> List[dict]:
    user_exercises = []
    for user_exercise in user_exercise_collection.find({"raceID": id}):
        user_exercises.append(user_exercise_helper(user_exercise))
    return user_exercises


# Update a user_exercise with a matching ID
def update_user_exercise(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user_exercise = user_exercise_collection.find_one({"_id": ObjectId(id)})
    if user_exercise:
        updated_user_exercise = user_exercise_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user_exercise:
            return True
        return False


# Delete a user_exercise from the database
def delete_user_exercise(id: str):
    user_exercise = user_exercise_collection.find_one({"_id": ObjectId(id)})
    if user_exercise:
        user_exercise_collection.delete_one({"_id": ObjectId(id)})
        return True
