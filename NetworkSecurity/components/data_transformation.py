import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from NetworkSecurity.constant.training_pipeline import TARGET_COLUMN
from NetworkSecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from NetworkSecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact

from NetworkSecurity.entity.config_entity import DataTransformationConfig
from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logger import logging

from NetworkSecurity.utils.main_utils.utils import save_object, save_numpy_array_data

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                  data_transformation_config:DataTransformationConfig):
          try:
               self.data_validation_artifact = data_validation_artifact
               self.data_transformation_config= data_transformation_config
          except Exception as e:
               raise CustomException(e,sys)
    
    @staticmethod # not dependent on DataTRansformation. write it outside class == write inside class using @staticmethod. 
    def read_data(file_path)-> pd.DataFrame:
         try:
              return pd.read_csv(file_path)
         except Exception as e :
              raise CustomException(e,sys)
        
    def get_data_transformater_object(cls)-> Pipeline:
         logging.info("entered get_data_transformer object inside DataTransformation class ")
         try:
              Imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
              logging.info(f"initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
              processor=Pipeline([("imputer", Imputer)])
              return processor

         except Exception as e:
              raise CustomException(e,sys)
          
    def intiate_data_transformation(self)-> DataTransformationArtifact:
         logging.info("Entered intiate_data_transformation method in DataTranformation Class")
         try:
            logging.info("starting intiate_data_transformation")
            logging.info("getting train and test df")
            train_df= DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            logging.info("removing target feature from train_df")
            train_target_column= train_df[TARGET_COLUMN]
            train_df= train_df.drop(columns=[TARGET_COLUMN],axis=1)
            train_target_column = train_target_column.replace(-1,0)
            
            logging.info("removing target feature")
            test_target_column= test_df[TARGET_COLUMN]
            test_df= test_df.drop(columns=[TARGET_COLUMN],axis=1)
            test_target_column = test_target_column.replace(-1,0)
            
            logging.info("transforming train and test data")
            processor = self.get_data_transformater_object()
            transformed_object = processor.fit(train_df)
            transformed_train_df= processor.transform(train_df)
            transformed_test_df = processor.transform(test_df)
            
            
            logging.info("combining input and target feature")
            train_data = np.c_[transformed_train_df, np.array(train_target_column)]
            test_data = np.c_[transformed_test_df, np.array(test_target_column)]
 
            logging.info("savning tranformed data ")
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_data)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_data)
            save_numpy_array_data(self.data_transformation_config.transformed_object_file_path,transformed_object)

            logging.info("preparing artifact")
            data_transformation_artifact= DataTransformationArtifact(
                 transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                 transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                 transformed_test_file_path= self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact

            
            

            



         except Exception as e:
               raise CustomException(e,sys)





 