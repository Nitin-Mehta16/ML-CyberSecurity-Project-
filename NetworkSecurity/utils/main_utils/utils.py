from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logger import logging
import yaml
import os,sys
import numpy as np
import dill
import pickle

def read_yaml_file(file_path:str) -> dict:
    try:
        logging.info("reading schema.yml")
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
        logging.info("read schema.yml")
    except Exception as e:
        raise CustomException(e,sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs (os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CustomException(e, sys)