from app.ml.base_model.movenet import movenet
from app.ml.preprocessing import preprocessing_image_movenet


class BaseTrainer(object):
    type_exercise: str

    def get_keypoints_std(self):
        """"""

    def _get_keypoints(self, input_image):
        input_image = preprocessing_image_movenet(input_image)
        keypoints_with_scores = movenet(input_image)
        return keypoints_with_scores

    def calculate_score(self):
        return 100
