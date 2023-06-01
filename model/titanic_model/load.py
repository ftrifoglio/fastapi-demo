import os
import pickle

import pandas as pd
from sklearn.model_selection import train_test_split

from .preprocessing import WithinGroupMeanImputer, make_more_features

this_dir, this_filename = os.path.split(__file__)
model_v1_path = os.path.join(this_dir, "assets/model_v1.pkl")
model_v2_path = os.path.join(this_dir, "assets/model_v2.pkl")
data_path = os.path.join(this_dir, "assets/train.csv")

with open(model_v1_path, "rb") as file:
    model_v1 = pickle.load(file)

with open(model_v2_path, "rb") as file:
    model_v2 = pickle.load(file)

train = pd.read_csv(data_path)
y = train["Survived"].copy()
X = train.drop("Survived", axis=1).copy()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=123
)
