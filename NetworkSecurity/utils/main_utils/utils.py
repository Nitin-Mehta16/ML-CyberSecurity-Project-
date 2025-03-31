from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logger import logging
import yaml
import os,sys
import numpy as np
import dill
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

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
    
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise CustomException(e, sys) 
    
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise CustomException(e, sys) from e
    

def load_object(file_path: str) -> object:
    try:
        logging.info("Entered the load_object method of MainUtils class")
        if not os.path.exists(file_path):
            raise Exception(f"The file {file_path} is not exist")
        with open(file_path,"rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise CustomException(e, sys) from e
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
    Load numpy array data to file
    file_path: str location of file to save
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test,models, params):
    try:
        report = {}
        print (params)
        print(models)

        for model_name , model_func in models.items():
            print(f"Starting model training for --> {model_func}")
            print(f"model params --> {params[model_name]}")
            param= params[model_name]

            gs = GridSearchCV(model_func, param, cv=3)
            gs.fit(X_train,y_train)

            print(gs.best_params_)
            model_func.set_params(**gs.best_params_)
            model_func.fit(X_train,y_train)

            y_train_pred = model_func.predict(X_train)
            y_test_pred = model_func.predict(X_test)

            train_model_socre = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)

            report[model_name] = test_model_score

        return report
    
    except Exception as e :
        raise CustomException (e,sys)