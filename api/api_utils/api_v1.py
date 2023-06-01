from typing import Annotated

import pandas as pd
from fastapi import APIRouter, Query
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
from titanic_model.load import X_test, model_v1, y_test

from .schemas import modelData

api_router_v1 = APIRouter()


@api_router_v1.post("/predict/")
def predict_survival(data: modelData):
    input = pd.DataFrame(data.dict(), index=[0])
    return model_v1.predict_proba(input)[0, 1]


@api_router_v1.get("/score/")
def get_score(
    type: Annotated[
        list[str],
        Query(
            title="Score type",
            description="Model accuracy, recall and ROC on the test set",
        ),
    ]
) -> dict:
    y_proba = model_v1.predict_proba(X_test)[:, 1]
    y_pred = model_v1.predict(X_test)
    scores = {
        "roc": roc_auc_score(y_test, y_proba),
        "recall": recall_score(y_test, y_pred),
        "accuracy": accuracy_score(y_test, y_pred),
    }
    found = set(type) & scores.keys()
    not_found = set(type) - scores.keys()
    r = {key: scores[key] for key in found}
    r.update({k: "not found" for k in not_found})
    return r
