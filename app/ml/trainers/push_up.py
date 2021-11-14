import numpy as np

from app.ml.trainers.base import BaseTrainer
from app.ml.utils import calculateAngle


class PushUpTrainer(BaseTrainer):
    type_exercise = 'push-up'

    def predict(self, image):
        keypoints_std = self.get_keypoints_std()

        keypoints_predict = self._get_keypoints(image)
        keypoints_predict = np.array([keypoints_predict[0][0][6],
                                      keypoints_predict[0][0][8],
                                      keypoints_predict[0][0][10]])

        angle_config = self.get_angle(keypoints_std)
        angle_predict = self.get_angle(keypoints_predict)

        return []

    def get_keypoints_std(self):
        return np.array([[0.4435669, 0.6497738, 0.5918565],
                         [0.5384197, 0.48176622, 0.61224455],
                         [0.66870534, 0.54405385, 0.6780684]])

    def get_angle(self, keypoints: list):
        return calculateAngle(*keypoints)
