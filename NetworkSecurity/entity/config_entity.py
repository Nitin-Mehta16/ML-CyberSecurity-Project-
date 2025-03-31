from datetime import datetime
import os
from NetworkSecurity.exception.exception import CustomException
import sys
from NetworkSecurity.constant import training_pipeline
from NetworkSecurity.logging.logger import logging

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

class training_pipeline_config:
    def __init__(self,timestamp=datetime.now()):
        try:
            logging.info("initating training pipeline config")
            timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
            self.pipeline_name=training_pipeline.PIPELINE_NAME
            self.artifact_name=training_pipeline.ARTIFACT_DIR
            self.artifact_dir=os.path.join(ROOT_DIR,self.artifact_name,timestamp)
            self.timestamp: str=timestamp
        except Exception as e:
            raise CustomException(e,sys)
        

class DataIngestionConfig:
    def __init__(self,training_pipeline_config=training_pipeline_config):
        try:
            logging.info("initiating data ingestion directory")
            self.data_ingestion_dir:str = os.path.join(
                training_pipeline_config.artifact_dir,
                training_pipeline.DATA_INGESTION_DIR_NAME
            #CyberSecurity-Project\Artifacts\09_16_2024_20_37_54\data_ingestion
            )
            logging.info("initating feature_store_file_path")
            self.feature_store_file_path: str = os.path.join(
                    self.data_ingestion_dir,
                    training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
                    training_pipeline.FILE_NAME
                    #\feature_store\phisingData.csv
            #CyberSecurity-Project\Artifacts\09_16_2024_20_37_54\data_ingestion\feature_store\phisingData.csv        
                )
            logging.info("initiating training_file_path")
            self.training_file_path: str = os.path.join(
                    self.data_ingestion_dir,
                    training_pipeline.DATA_INGESTION_INGESTED_DIR,
                    training_pipeline.TRAIN_FILE_NAME
                    #\ingested\train.csv
            #CyberSecurity-Project\Artifacts\09_16_2024_20_37_54\data_ingestion\ingested\train.csv
                )
            logging.info("initiating testing_file_path")
            self.testing_file_path: str = os.path.join(
                    self.data_ingestion_dir,
                    training_pipeline.DATA_INGESTION_INGESTED_DIR,
                    training_pipeline.TEST_FILE_NAME
                    #\ingested\test.csv
            #CyberSecurity-Project\Artifacts\09_16_2024_20_37_54\data_ingestion\ingested\test.csv
                )
            logging.info("initiating train_test_split_ratio ")
            self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
            logging.info("initiating collection_name")
            self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
            logging.info("initiating database_name")
            self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME
        except Exception as e:
            raise CustomException(e,sys)

class DataValidationConfig:
    def __init__(self,training_pipeline_config=training_pipeline_config):
        try:
            logging.info("Initiating Data Validation Config")
            self.data_validation_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME)
            self.valid_data_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_NAME)
            self.invalid_data_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_NAME)
            self.valid_train_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
            self.valid_test_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
            self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
            self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)
            self.drift_report_file_path: str = os.path.join(
                self.data_validation_dir,
                training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
            )
        except Exception as e:
            raise CustomException(e,sys)
    
class DataTransformationConfig:
     def __init__(self,training_pipeline_config:training_pipeline_config):
        self.data_transformation_dir: str = os.path.join( training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME )
        self.transformed_train_file_path: str = os.path.join( self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),)
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,  training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy"), )
        self.transformed_object_file_path: str = os.path.join( self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME)

class ModelTrainerConfig:
    def __init__(self, training_pipeline_config:training_pipeline_config):
        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME
        )
        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME
        )
        self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold = training_pipeline.MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD
