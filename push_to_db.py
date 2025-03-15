import os
import json 
import sys

from dotenv import load_dotenv
load_dotenv()

Mongo_DB_URL = os.getenv("MONGO_DB_URL")
print(Mongo_DB_URL)

import certifi  # python package provide with set of root certificates 
ca= certifi.where()  # consist of bundle of certificates for verifying request is comming from trusted/secure connection

import pandas as pd 
import numpy as np 
import pymongo 
from NetworkSecurity.logging.logger import logging 
from NetworkSecurity.exception.exception import CustomException

class DataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e :
            raise CustomException(e,sys)
        
    def csv_to_json(self,file_path):
        try:
            data= pd.read_csv(file_path)
            logging.info("read the csv")

            logging.info("removing index from the data")
            data.reset_index(drop=True,inplace=True)
            logging.info("converting csv to json")
            records = list(json.loads(data.T.to_json()).values())
            logging.info("conversion of data into json is done")
            return records


        except Exception as e:
            raise CustomException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.records= records
            self.database=database
            self.collection=collection
            
            logging.info("Connecting to monogo")
            self.mongo_client=pymongo.MongoClient(Mongo_DB_URL)
            logging.info("Creating database")
            self.database= self.mongo_client[self.database]
            logging.info("Creating collection")
            self.collection= self.database[self.collection]
            logging.info("Creating records")
            self.collection.insert_many(self.records)
            logging.info("Insertion inside mongo done")
            return (len(self.records))
            
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    FILE_PATH = "Network_data\phisingData.csv"
    DATABASE ="ML_PROJECT"
    COLLECTION= "PHISING_DATA"
    data_extract = DataExtract()
    records=data_extract.csv_to_json(FILE_PATH)
    print(records)
    length_of_records= data_extract.insert_data_mongodb(records,DATABASE,COLLECTION) 
    print(length_of_records)




