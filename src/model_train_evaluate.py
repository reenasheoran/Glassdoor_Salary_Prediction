import os
import warnings
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from load_data import read_params
import argparse
import joblib
import json

def evaluate_model(actual, predicted):
    MAE = np.round(mean_absolute_error(actual, predicted),3)
    return MAE

def train_model(config_path):
    config = read_params(config_path)
    
    train_data_path = config["split_data"]["train_path"]
    test_data_path = config["split_data"]["test_path"]
    train = pd.read_csv(train_data_path, sep=",")
    test = pd.read_csv(test_data_path, sep=",")
    target = config["base"]["target"]   
 
    X_train = train.drop(target, axis=1)
    X_test = test.drop(target, axis=1)
    Y_train = train[target]
    Y_test = test[target]

    random_state = config["base"]["random_state"]
    criterion = config["estimators"]["RandomForest"]["params"]["criterion"]
    n_estimators = config["estimators"]["RandomForest"]["params"]["n_estimators"]

    RF = RandomForestRegressor(criterion=criterion, n_estimators=n_estimators)
    RF.fit(X_train,Y_train)
    Y_pred = RF.predict(X_test)

    MAE = evaluate_model(Y_test,Y_pred)

    print("RandomForest model (criterion=%s, n_estimators=%f):" % (criterion,n_estimators))
    
    print("  MAE: %s" % MAE)
    

    model_dir = config["model_dir"]

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")

    joblib.dump(RF, model_path)

    scores_file = config["report"]["scores"]
    
    with open(scores_file, "w") as f:
        scores = {
             
             "MAE": MAE
        }
        json.dump(scores, f, indent=4)
    
    params_file = config["report"]["params"]

    with open(params_file, "w") as f:
        params = {
            "criterion": criterion,
            "n_estimators": n_estimators
        }
        json.dump(params, f, indent=4)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_model(config_path=parsed_args.config)