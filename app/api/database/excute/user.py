from typing import List

from bson.objectid import ObjectId

from app.api.database.connect import user_collection
from app.api.helpers.convert_model2dict import user_helper


# Retrieve all users present in the database
def retrieve_users():
    users = []
    for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Add a new user into to the database
def add_user(user_data: dict) -> dict:
    user = user_collection.insert_one(user_data)
    new_user = user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


# Retrieve a user with a matching ID
def retrieve_user(id: str) -> dict:
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


# Retrieve a user with a matching ID
def retrieves_user_by_race_id(id: str) -> List[dict]:
    users = []
    for user in user_collection.find({"raceID": id}):
        users.append(user_helper(user))
    return users


# Update a user with a matching ID
def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# Delete a user from the database
def delete_user(id: str):
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        user_collection.delete_one({"_id": ObjectId(id)})
        return True
