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

        

