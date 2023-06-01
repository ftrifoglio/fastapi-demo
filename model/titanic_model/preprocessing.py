from typing import Self

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class WithinGroupMeanImputer(BaseEstimator, TransformerMixin):
    """Imputes missing values within groups with the mean of the group."""

    def __init__(self, group_var: str) -> None:
        """
        Parameters
        ----------
        group_var : {str}
            The name of the grouping variable.
        """
        self.group_var = group_var

    def fit(self, X: pd.DataFrame, y: pd.DataFrame = None) -> Self:
        """Fit the imputer on `X`.

        Parameters
        ----------
        X : {dataframe}, shape (n_samples, n_features)
            Input data, where `n_samples` is the number of samples and
            `n_features` is the number of features.

        y : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        self : object
            Fitted estimator.
        """
        self.statistics_ = X.groupby(self.group_var).mean(numeric_only=True)
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Impute all missing values in `X`.

        Parameters
        ----------
        X : {dataframe}, shape (n_samples, n_features)
            The input data to complete.

        Returns
        -------
        X_imputed : {dataframe}, shape (n_samples, n_features_out)
            `X` with imputed values.
        """
        X_ = X.copy()
        for col in X_.columns:
            if col != self.group_var:
                X_.loc[(X[col].isna()) & X_[self.group_var].notna(), col] = X_[
                    self.group_var
                ].map(self.statistics_[col])
        X_imputed = X_.drop([self.group_var], axis=1)
        return X_imputed

    def get_feature_names_out(self) -> None:
        pass


def make_more_features(X: pd.DataFrame) -> pd.DataFrame:
    """
    Add two more features.

    num__Child is a binary feature (whether passenger was <= 16)
    num__Family is a numeric feature (number of family members on board)
    num__Age is left as is

    Parameters
    ----------
    X : {dataframe}, shape (n_samples, n_features)
        The input data to complete.

    Returns
    -------
    X_engineered : {dataframe}, shape (n_samples, n_features_out)
        `X` with engineered values.
    """
    X_ = X.copy()
    X_["num__Child"] = np.where(X_["num__Age"] <= 16, 1, 0)
    X_["num__Family"] = X_["num__SibSp"] + X_["num__Parch"] + 1
    X_engineered = X_.drop(["num__SibSp", "num__Parch"], axis=1)
    return X_engineered
