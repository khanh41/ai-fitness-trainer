from typing import List

from bson.objectid import ObjectId

from app.api.database.connect import user_information_collection
from app.api.helpers.convert_model2dict import user_information_helper


# Retrieve all user_informations present in the database
def retrieve_user_informations():
    user_informations = []
    for user_information in user_information_collection.find():
        user_informations.append(user_information_helper(user_information))
    return user_informations


# Add a new user_information into to the database
def add_user_information(user_information_data: dict) -> dict:
    user_information = user_information_collection.insert_one(user_information_data)
    new_user_information = user_information_collection.find_one({"_id": user_information.inserted_id})
    return user_information_helper(new_user_information)


# Retrieve a user_information with a matching ID
def retrieve_user_information(id: str) -> dict:
    user_information = user_information_collection.find_one({"_id": ObjectId(id)})
    if user_information:
        return user_information_helper(user_information)


# Retrieve a user_information with a matching ID
def retrieves_user_information_by_race_id(id: str) -> List[dict]:
    user_informations = []
    for user_information in user_information_collection.find({"raceID": id}):
        user_informations.append(user_information_helper(user_information))
    return user_informations


# Update a user_information with a matching ID
def update_user_information(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user_information = user_information_collection.find_one({"_id": ObjectId(id)})
    if user_information:
        updated_user_information = user_information_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user_information:
            return True
        return False


# Delete a user_information from the database
def delete_user_information(id: str):
    user_information = user_information_collection.find_one({"_id": ObjectId(id)})
    if user_information:
        user_information_collection.delete_one({"_id": ObjectId(id)})
        return True
