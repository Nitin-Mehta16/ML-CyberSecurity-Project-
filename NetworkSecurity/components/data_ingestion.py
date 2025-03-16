from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logger import logging
#configuration of data ingestion config 
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact

import os 
import sys 
import numpy as np 
import pandas as pd
import pymongo 
from typing import List 
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()
logging.info("collecting  mongo url")
mongo_url = os.getenv("MONGO_DB_URL")



class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config   
        except Exception as e:
            raise CustomException(e,sys)
            
    def export_collection_as_df(self):
        logging.info("importing mongo data in dataframe form ")
        try:
            db_name= self.data_ingestion_config.database_name
            collection_name= self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(mongo_url)
            collection=self.mongo_client[db_name][collection_name]

            df=pd.DataFrame(list(collection.find()))
            df.drop(columns=['_id'],axis=1,inplace=True)
            df.replace({"na":np.nan},inplace=True)

            return df
        
        except Exception as e:
            raise CustomException(e,sys)
    
    def store_data_into_feature_dir(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            logging.info("Creating feature_store_file_path")
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info("Storing data into feature_store_file_path in dataframe format")
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise CustomException(e, sys)
        
    def split_data_as_train_test(self,df:pd.DataFrame):
        try:
            train_set, test_set = train_test_split(df,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train Test Split")
            
            logging.info("making training_file_path")
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
    
            logging.info("making testing_file_path")
            dir_path=os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info("Storing training data into training file path")
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,index=False,header=True
            )
            logging.info("Storing testing data into testing file path")
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,index=False,header=True
            )
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_ingestion(self):
        try:
            df = self.export_collection_as_df()
            df = self.store_data_into_feature_dir(df)
            self.split_data_as_train_test(df)
            
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                          test_file_path = self.data_ingestion_config.testing_file_path
                                                          )
            return data_ingestion_artifact
            # return  self.data_ingestion_config.training_file_path,self.data_ingestion_config.testing_file_path
 
        except Exception as e:
            raise CustomException(e,sys)
