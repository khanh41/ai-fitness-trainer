from app.api.database.connect import exercise_trainer_collection
from app.api.database.execute.base_execute import BaseExecute
from app.api.helpers.convert_model2dict import exercise_trainer_helper


class ExerciseTrainerExecute(BaseExecute):

    def __init__(self, data_collection, data_helper):
        super().__init__(data_collection, data_helper)

    def delete_by_exercise_id(self, exercise_id):
        data = self.data_collection.find_one({"exerciseId": exercise_id})
        if data:
            self.data_collection.delete_one({"exerciseId": exercise_id})
            return True

    # Retrieve a data with a matching exerciseId
    def retrieve_data_by_exercise_id(self, exercise_id: str) -> dict:
        data = self.data_collection.find_one({"exerciseId": exercise_id})
        if data:
            return self.data_helper(data)


exercise_trainer_execute = ExerciseTrainerExecute(exercise_trainer_collection, exercise_trainer_helper)
