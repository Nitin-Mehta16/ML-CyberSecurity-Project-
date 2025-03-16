from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.config_entity import training_pipeline_config
from NetworkSecurity.components.data_validation import DataValidation, DataValidationConfig

from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logger import logging
import sys

if __name__ == "__main__":
    try:
        logging.info("calling training_pipeline_config()")
        training_pipeline_config = training_pipeline_config()
        logging.info("calling DataIngestionConfig() ")
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        logging.info("calling DataIngestion() ")
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("initiate_data_ingestion")
        DataIngestionArtifact = data_ingestion.initiate_data_ingestion()
        # print(DataIngestionArtifact)
        logging.info("initiate_data_validation")
        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation=DataValidation(DataIngestionArtifact,data_validation_config)
        logging.info("data_validation........")
        data_validation = data_validation.initiate_data_validation()
        print(data_validation)
    except Exception as e:
        raise CustomException(e,sys)