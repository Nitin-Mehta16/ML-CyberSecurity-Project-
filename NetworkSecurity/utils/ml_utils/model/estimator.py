from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_TRAINER_TRAINED_MODEL_NAME

import os
import sys

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise CustomException(e, sys)
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_pred = self.model.predict(x_transform)
            return y_pred
        except Exception as e:
            raise CustomException(e, sys)
