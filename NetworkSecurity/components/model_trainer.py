import sys
import os

from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logger import logging

from NetworkSecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from NetworkSecurity.entity.config_entity import ModelTrainerConfig

from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel
from NetworkSecurity.utils.main_utils.utils import save_object, load_object
from NetworkSecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_models
from NetworkSecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
                                AdaBoostClassifier,
                                GradientBoostingClassifier,
                                RandomForestClassifier,
                                )

import mlflow 

import numpy as np
import pandas as pd 
from sklearn.pipeline import Pipeline

class ModelTrainer:
    def __init__ (self,model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def track_mlflow(self, best_model, classification_matrics):
        with mlflow.start_run():
            f1_score = classification_matrics.f1_score
            precision_score = classification_matrics.precision_score
            recall_score = classification_matrics.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)

            mlflow.sklearn.log_model(best_model, "model")



        
    def train_model(self,x_train,y_train,x_test,y_test):
        models = {
            # "Random Forest": RandomForestClassifier (verbose=1),
            "Decision_Tree": DecisionTreeClassifier(),
            # "Gradient Boosting": GradientBoostingClassifier (verbose=1),
            # "Logistic Regression": LogisticRegression (verbose=1),
            # "AdaBoost": AdaBoostClassifier(),
        }

        params={
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Decision_Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }        
        }
        
        model_report:dict=evaluate_models(X_train=x_train,y_train=y_train,X_test=x_test,y_test=y_test,
                                          models=models,params=params)
        print(f"model_report --> {model_report}")
        
        best_model_score =  max(sorted(model_report.values()))

        best_model_name = [key  for key,value in model_report.items() if value==best_model_score ]

        best_model = models[best_model_name[0]]
        print(f"best_model --> {best_model}")
        print(f"best_model_score --> {best_model_score}")

        y_train_pred = best_model.predict(x_train)
        classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
        print(f"classification_train_metric --> {classification_train_metric}")

        ##Track the mlflow 
        self.track_mlflow(best_model,classification_train_metric)

        y_test_pred=best_model.predict(x_test)
        classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
        print(f"classification_test_metric --> {classification_test_metric}")
 
        ##Track the mlflow 
        self.track_mlflow(best_model,classification_test_metric)

        
        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=Network_Model)

        save_object("final_model/model.pkl",best_model)

        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=classification_test_metric
                             )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact




        
        
    def initiate_model_trainer(self)-> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_df = load_numpy_array_data(train_file_path)
            test_df = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_df[:,:-1],
                train_df[:,-1],
                test_df[:,:-1],
                test_df[:,-1],
            )

            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            print(model_trainer_artifact)

        except Exception as e:
            raise CustomException(e,sys)




  