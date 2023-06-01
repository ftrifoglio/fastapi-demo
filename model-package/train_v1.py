import pickle

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler
from titanic_model.load import X_test, X_train, y_test, y_train
from titanic_model.preprocessing import WithinGroupMeanImputer, make_more_features

imputer = ColumnTransformer(
    [
        ("cat", SimpleImputer(strategy="most_frequent"), ["Pclass", "Sex", "Embarked"]),
        ("num", WithinGroupMeanImputer("Pclass"), ["Age", "SibSp", "Parch", "Pclass"]),
    ]
)
imputer.set_output(transform="pandas")
feature_maker = ColumnTransformer(
    [
        (
            "new",
            FunctionTransformer(make_more_features),
            ["num__Age", "num__SibSp", "num__Parch"],
        ),
        (
            "ohe",
            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ["cat__Pclass", "cat__Sex", "cat__Embarked"],
        ),
    ]
)
scaler = ColumnTransformer(
    [("num", StandardScaler(), slice(0, 3))], remainder="passthrough"
)
model = LogisticRegression(random_state=123)
pipeline = Pipeline(
    [("impute", imputer), ("make", feature_maker), ("sacle", scaler), ("model", model)]
)

penalty = ["l1", "l2"]
C = np.logspace(-5, 5, 50)
param_grid = {"model__penalty": penalty, "model__C": C, "model__solver": ["liblinear"]}
cv = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=2)

if __name__ == "__main__":
    cv.fit(X_train, y_train)
    y_proba = cv.predict_proba(X_test)[:, 1]
    y_pred = cv.predict(X_test)
    scores = {
        "roc": roc_auc_score(y_test, y_proba),
        "recall": recall_score(y_test, y_pred),
        "accuracy": accuracy_score(y_test, y_pred),
    }
    print(scores)
    with open("titanic_model/assets/model_v1.pkl", "wb+") as file:
        pickle.dump(cv, file)
