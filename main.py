from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.entity.config_entity import training_pipeline_config, DataValidationConfig, DataTransformationConfig, DataIngestionConfig
from NetworkSecurity.components.data_validation import DataValidation, DataValidationConfig,DataValidationArtifact
from NetworkSecurity.components.model_trainer import ModelTrainerConfig, ModelTrainer
from NetworkSecurity.components.data_transformation import DataTransformation

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
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("data_transformation........")
        data_transformation_config= DataTransformationConfig(training_pipeline_config)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact = data_transformation.intiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("data_trainer........")
        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        logging.info("Model Training artifact created")
                


    except Exception as e:
        raise CustomException(e,sys)