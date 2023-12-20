""" Testing utilities that allow for easier assertions on collections.
Do you love tests? Neither do we.
"""
# TODO: This module due is for a refactor.
from typing import Any
import numbers
import numpy as np
import torch
import pandas as pd
from scipy.sparse import csc_matrix
from scipy.sparse import csr_matrix
from scipy.sparse import dok_matrix
from scipy.sparse import lil_matrix


def coerced(o: Any):
    if isinstance(o, (csc_matrix, csr_matrix, dok_matrix, lil_matrix)):
        o = o.toarray()

    to_list_collections = tuple([np.ndarray, torch.Tensor, pd.core.series.Series])
    if isinstance(o, (list, tuple)):
        return o
    elif isinstance(o, to_list_collections):
        return o.tolist()
    elif isinstance(o, pd.core.frame.DataFrame):
        return o.values.tolist()
    elif isinstance(o, dict):
        li = [np.nan] * len(o)
        for k, v in o.items():
            li[k] = v
        return li
    else:
        raise ValueError(f"Object {o} of {type(o)} is not a list, tuple nor array.")


def is_close(
    a: numbers.Number, b: numbers.Number, rel_tol: float = 1e-09, abs_tol: float = 0.0
):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def ctr_eq(c1: Any, c2: Any):
    if isinstance(c1, torch.Tensor) and c1.shape == torch.Size([]):
        c1 = c1.item()
    if isinstance(c2, torch.Tensor) and c2.shape == torch.Size([]):
        c2 = c2.item()

    if isinstance(c1, numbers.Number) and isinstance(c2, numbers.Number):
        return is_close(c1, c2)

    c1 = coerced(c1)
    c2 = coerced(c2)

    return all([ctr_eq(c1[i], c2[i]) for i in range(max(len(c1), len(c2)))])
