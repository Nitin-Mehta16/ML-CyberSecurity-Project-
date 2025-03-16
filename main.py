from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.config_entity import training_pipeline_config

from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logger import logging
import sys

if __name__ == "__main__":
    try:
        logging.info("calling training_pipeline_config() ")
        training_pipeline_config = training_pipeline_config()
        logging.info("calling DataIngestionConfig() ")
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        logging.info("calling DataIngestion() ")
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("initiate_data_ingestion")
        DataIngestionArtifact = data_ingestion.initiate_data_ingestion()
        print(DataIngestionArtifact)
    except Exception as e:
        raise CustomException(e,sys)