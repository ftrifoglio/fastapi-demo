import pickle

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.experimental import enable_halving_search_cv
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
from sklearn.model_selection import HalvingGridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder
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
model = RandomForestClassifier(random_state=123)
pipeline = Pipeline([("impute", imputer), ("make", feature_maker), ("model", model)])

max_depth = list(np.arange(50, 91, 10))
min_samples_split = [5, 10, 15]
min_samples_leaf = [2, 4, 6]
param_grid = {
    "model__max_depth": max_depth,
    "model__min_samples_split": min_samples_split,
    "model__min_samples_leaf": min_samples_leaf,
}
cv = HalvingGridSearchCV(
    pipeline,
    param_grid,
    resource="model__n_estimators",
    min_resources=500,
    max_resources=2000,
    factor=2,
    cv=5,
    n_jobs=-1,
    verbose=2,
)

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
    with open("titanic_model/assets/model_v2.pkl", "wb+") as file:
        pickle.dump(cv, file)
