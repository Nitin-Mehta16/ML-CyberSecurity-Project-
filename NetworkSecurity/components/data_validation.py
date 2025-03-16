from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact
from NetworkSecurity.entity.config_entity import DataValidationConfig
from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from NetworkSecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

from scipy.stats import ks_2samp #for checking data drift 
import pandas as pd 
import numpy as np
import os, sys

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            logging.info("Intitialing Data Validation..........")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            logging.info("Storing schema file................")
            self.schema_file = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys )
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)

    def validation_number_of_columns(self,df:pd.DataFrame)-> bool:
        try:
            number_of_columns=len(self.schema_file)
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data frame columns:{len(df.columns)}")
            if len(df.columns)==number_of_columns:
                return True
            return False
        except Exception as e:
            raise CustomException(e,sys)
    
    def numerical_column_exist(self,df:pd.DataFrame):
        try:
            numerical_columns = df.select_dtypes(include=[np.number]).columns
            number_of_numerical_columns = len(numerical_columns)
            if(number_of_numerical_columns>0):
                return True
            return False
        except Exception as e:
            raise CustomException(e,sys)

    def detect_dataset_drift(self, base_df,current_df,thershold=0.5) -> bool:
        try:
            logging.info("detecting data drift")
            status=True
            report={}
            for i in base_df.columns:
                d1=base_df[i]
                d2=current_df[i]
                is_sample_dist = ks_2samp(d1,d2)
                if thershold<= is_sample_dist.pvalue:
                    is_found=False
                else:
                    is_found = True
                    status = True
                report.update({i:{
                    "p_value":float(is_sample_dist.pvalue),
                    "drift_status":is_found
                }})
            logging.info("Creating data drift report")
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("Writing data drift report")
            write_yaml_file(file_path=drift_report_file_path,content=report)
            
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path= self.data_ingestion_artifact.trained_file_path
            test_file_path= self.data_ingestion_artifact.test_file_path

            logging.info("reading the data from train and test path")
            train_df= DataValidation.read_data(train_file_path)
            test_df= DataValidation.read_data(test_file_path)

            logging.info("validating number of columns")
            status=self.validation_number_of_columns(train_df)
            if not status:
                error_message=f"Train dataframe does not contain all columns. \n"
                logging.error(error_message)
            status=self.validation_number_of_columns(test_df)
            if not status:
                error_message=f"Test dataframe does not contain all columns. \n"
                logging.error(error_message)

            logging.info("checking wheather numerical column exist of not")
            numerical_column_exist = self.numerical_column_exist(train_df)
            if not numerical_column_exist:
                error_message=f"Train dataframe does not contain numerical columns. \n"
                logging.error(error_message)
            numerical_column_exist = self.numerical_column_exist(test_df)
            if not numerical_column_exist:
                error_message=f"Test dataframe does not contain numerical columns. \n"
                logging.error(error_message)
            
            logging.info("Initiating Data Drift check..................")
            status=self.detect_dataset_drift(base_df=train_df,current_df=test_df)
            
            logging.info("Storing Valid Drift Data into valid_data folder")
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_df.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            return data_validation_artifact
            
            
        except Exception as e:
            raise CustomException(e,sys)


