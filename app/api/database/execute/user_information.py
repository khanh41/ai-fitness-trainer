from app.api.database.connect import user_information_collection
from app.api.database.execute.base_execute import BaseExecute
from app.api.helpers.convert_model2dict import user_information_helper


class ExerciseTrainerExecute(BaseExecute):

    def __init__(self, data_collection, data_helper):
        super().__init__(data_collection, data_helper)

    # Retrieve a data with a matching email
    def retrieve_data_by_user_id(self, user_id: str) -> dict:
        data = self.data_collection.find_one({"userId": user_id})
        if data:
            return self.data_helper(data)


user_information_execute = ExerciseTrainerExecute(user_information_collection, user_information_helper)
