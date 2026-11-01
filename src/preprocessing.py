import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

from src.features import CORE_FEATURES, LINEAR_FEATURES


#log of 1 plus the absolute value with the sign kept so zeros are allowed
def signed_log(x):
    return np.sign(x) * np.log1p(np.abs(x))


#log then scale then median impute with 0 or 1 missing indicators
def _branch(log, scale):
    steps = []
    if log:
        steps.append(("signed_log", FunctionTransformer(signed_log, feature_names_out="one-to-one")))
    if scale:
        steps.append(("scale", StandardScaler()))
    steps.append(("impute", SimpleImputer(strategy="median", add_indicator=True)))
    return Pipeline(steps)


#preprocessor for the given features with scale set to False for tree models
def build_preprocessor(features=CORE_FEATURES, scale=True):
    log_cols = [c for c in features if c not in LINEAR_FEATURES]
    linear_cols = [c for c in features if c in LINEAR_FEATURES]
    return ColumnTransformer(
        [("log", _branch(log=True, scale=scale), log_cols),
         ("linear", _branch(log=False, scale=scale), linear_cols)],
        verbose_feature_names_out=False,
    )
