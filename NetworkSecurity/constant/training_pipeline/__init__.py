import os
import sys
import numpy as np 
import pandas as pd

'''
defining common constant variable for training pipeline
'''
TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
SCHEMA_FILE_PATH = os.path.join(ROOT_DIR,"data_schema","schema.yaml")
SAVED_MODEL_DIR =os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"
PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"

'''
Data Ingestion related constant
'''
DATA_INGESTION_COLLECTION_NAME: str = "PHISING_DATA"
DATA_INGESTION_DATABASE_NAME: str = "ML_PROJECT"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

'''
Data Validation related constant
'''
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_NAME:str = "validated" #valid data
DATA_VALIDATION_INVALID_NAME:str = "invalid" #invalid data
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report" #changes happening in data with new data comming
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "drift_report.yaml"




"""
Data Transformation related constant start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"


## kkn imputer to replace nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"

DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"



'''
Model Trainer ralated constant start with MODE TRAINER VAR NAME
'''
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD: float = 0.05
