import math

import numpy as np

from app.utils.constants import ANGLE_TO_CALCULATE


class ScoreAngleCalculate:
    def __init__(self) -> None:
        pass

    def score_calculate(self, angle_model, angle_input):
        score = []
        for i in range(len(angle_model)):
            score.append(1 - abs((angle_model[i] - angle_input[i]) / 180))
        return np.array(score)

    def angle_pose(self, model_features):
        angle_model = []

        for point_a, point_b in ANGLE_TO_CALCULATE:
            vector_1 = model_features[point_a[1]] - model_features[point_a[0]]
            vector_2 = model_features[point_b[1]] - model_features[point_b[0]]
            angle_model.append(
                self.angle_of_two_vector(vector_1, vector_2) * 180 / math.pi
            )
        return angle_model

    def angle_of_two_vector(self, vector_1, vector_2):
        unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
        unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        return np.arccos(dot_product)

    def find_new_point(self, vector_a, vector_c, alpha, operator):
        alpha = alpha * 3.14 / 180
        a1, a2 = vector_a
        c1, c2 = vector_c

        A1 = c1 - a1
        A2 = c2 - a2

        C0 = A1 ** 2 + A2 ** 2
        C1 = math.cos(alpha) * C0

        A = (A2 / A1) ** 2 + 1
        B = -2 * C1 * A2 / A1 ** 2
        C = C1 ** 2 / A1 ** 2 - C0
        DENTA = B ** 2 - 4 * A * C

        B2 = (-B + operator * math.sqrt(DENTA)) / (2 * A)
        B1 = (C1 - B2 * A2) / A1

        b1 = B1 + a1
        b2 = B2 + a2

        return b1, b2

    def find_new_point_all(self, score, angle_model, angle_input, input_features):
        for i in range(len(score)):
            if score[i]:
                _, point_b = ANGLE_TO_CALCULATE[i]
                angle = angle_model[i] - angle_input[i]
                input_features[point_b[1]] = self.find_new_point(
                    input_features[point_b[0]],
                    input_features[point_b[1]],
                    abs(angle),
                    angle / angle,
                )
        return input_features
