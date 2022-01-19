from app.api.database.connect import exercise_collection
from app.api.database.execute.base_execute import BaseExecute
from app.api.helpers.convert_model2dict import exercise_helper


class ExerciseExecute(BaseExecute):

    def __init__(self, data_collection, data_helper):
        super().__init__(data_collection, data_helper)

    # Retrieve a data with a matching email
    def retrieve_data_by_name(self, name: str) -> dict:
        data = self.data_collection.find_one({"name": name})
        if data:
            return self.data_helper(data)


exercise_execute = ExerciseExecute(exercise_collection, exercise_helper)
