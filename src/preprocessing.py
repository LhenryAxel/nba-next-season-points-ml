import numpy as np
import pandas as pd


def normalize_categorical_missing(X):
    X = X.copy()

    if isinstance(X, pd.DataFrame):
        X = X.astype(object)
        X = X.where(
            pd.notna(X),
            np.nan
        )

    else:
        X = np.asarray(
            X,
            dtype=object
        )

        X[
            pd.isna(X)
        ] = np.nan

    return X
