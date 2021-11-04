import pymongo

from app.core.constant import MONGO_DETAILS

client = pymongo.MongoClient(MONGO_DETAILS, serverSelectionTimeoutMS=5000)
database = client.gym_trainer_db

exercise_collection = database.get_collection("exercise")
exercise_process_collection = database.get_collection("exercise_process")
exercise_trainer_collection = database.get_collection("exercise_trainer")
user_collection = database.get_collection("user")
user_exercise_collection = database.get_collection("user_exercise")
user_information_collection = database.get_collection("user_information")
