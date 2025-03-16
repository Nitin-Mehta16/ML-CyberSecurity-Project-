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





