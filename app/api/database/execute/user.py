from app.api.database.connect import user_collection
from app.api.database.execute.base_execute import BaseExecute
from app.api.helpers.convert_model2dict import user_helper


class UserExecute(BaseExecute):

    def __init__(self, data_collection, data_helper):
        super().__init__(data_collection, data_helper)


user_execute = UserExecute(user_collection, user_helper)
