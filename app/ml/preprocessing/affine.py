import numpy as np
from scipy.signal import savgol_filter


class DataPreprocessing:
    def __init__(self) -> None:
        pass

    def affine_transform(self, model_features, input_features):
        # In order to solve the augmented matrix (incl translation),
        # it's required all vectors are augmented with a "1" at the end
        # -> Pad the features with ones, so that our transformation can do translations too
        pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))])
        unpad = lambda x: x[:, :-1]

        # Pad to [[ x y 1] , [x y 1]]
        Y = pad(model_features)
        X = pad(input_features)

        # Solve the least squares problem X * A = Y
        # and find the affine transformation matrix A.
        A, res, rank, s = np.linalg.lstsq(X, Y)
        A[np.abs(A) < 1e-10] = 0  # set really small values to zero

        # Now we have found the augmented matrix A
        # we can display the input on the model = X'
        transform = lambda x: unpad(np.dot(pad(x), A))

        # Image of input pose onto model pose
        input_transform = transform(input_features)

        return input_transform

    def apply_filter(self, data_kp):
        data_new = data_kp.copy()

        for i in data_new.columns:
            if (i + 1) % 3 != 0:
                data_new[i] = savgol_filter(data_new[i], 25, 3, mode='nearest')
            # else:
            #   data_new[i] = -1

        return data_new
