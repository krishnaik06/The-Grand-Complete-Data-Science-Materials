# data_tool.py
import pandas as pd
import numpy as np
import re
import sqlite3
from pathlib import Path
from typing import Optional, List, Tuple, Union
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

# Unified preprocessing function

def preprocess_data(
    filepath_or_df: Union[str, pd.DataFrame],
    drop_cols: Optional[List[str]] = None,
    drop_null: bool = False,
    fill_null_with_zero: bool = False,
    column_to_clean: Optional[str] = None,
    address_col_to_standardize: Optional[str] = None,
    old_str: Optional[str] = None,
    new_str: Optional[str] = None,
    label_encode_cols: Optional[List[str]] = None,
    one_hot_encode_cols: Optional[List[str]] = None,
    one_hot_encode_cols_sklearn: Optional[List[str]] = None,
    scale: bool = False,
    axis_concat: Optional[int] = None,
    concat_cols: Optional[Tuple[Union[str, int], Union[str, int]]] = None,
    anomaly_col_train: Optional[str] = None,
) -> pd.DataFrame:
    # ✅ Accept either a filepath or a DataFrame
    if isinstance(filepath_or_df, pd.DataFrame):
        df = filepath_or_df.copy()
    else:
        df = read_data(filepath_or_df)

    df.drop_duplicates(inplace=True)

    if drop_cols:
        df.drop(columns=drop_cols, inplace=True)
    if drop_null:
        df.dropna(inplace=True)
    if fill_null_with_zero:
        df.fillna(0, inplace=True)
    if column_to_clean:
        df[column_to_clean] = df[column_to_clean].apply(
            lambda x: re.sub(r"[^a-zA-Z0-9]", "", str(x)) if pd.notnull(x) else x
        )
    if address_col_to_standardize and old_str is not None and new_str is not None:
        df[address_col_to_standardize] = df[address_col_to_standardize].apply(
            lambda x: str(x).replace(old_str, new_str) if pd.notnull(x) else x
        )

    if label_encode_cols:
        le = LabelEncoder()
        for col in label_encode_cols:
            if col in df.columns:
                df[col] = le.fit_transform(df[col].astype(str))

    if one_hot_encode_cols_sklearn:
        oe = OneHotEncoder(sparse_output=False)
        for col in one_hot_encode_cols_sklearn:
            encoded = oe.fit_transform(df[[col]])
            df = df.drop(columns=[col])
            df[oe.get_feature_names_out([col])] = encoded

    if one_hot_encode_cols:
        df = pd.get_dummies(df, columns=one_hot_encode_cols)

    if scale:
        scaler = StandardScaler()
        df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    if anomaly_col_train:
        scaler = StandardScaler()
        df[anomaly_col_train] = scaler.fit_transform(df[[anomaly_col_train]])
        df = df[(df[anomaly_col_train] <= 3) & (df[anomaly_col_train] >= -3)]

    if concat_cols and axis_concat is not None:
        df = pd.concat(
            [df[[concat_cols[0]]], df[[concat_cols[1]]]],
            axis=axis_concat,
            ignore_index=True,
        )

    return df



def read_data(filepath: str) -> pd.DataFrame:
    suffix = Path(filepath).suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(filepath)
    elif suffix == ".xlsx":
        return pd.read_excel(filepath)
    elif suffix == ".sql":
        conn = sqlite3.connect(filepath)
        df = pd.read_sql("SELECT * FROM table_name", conn)
        conn.close()
        return df
    elif suffix == ".json":
        return pd.read_json(filepath)
    elif suffix == ".parquet":
        return pd.read_parquet(filepath)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")

def preview(filepath: str):
    df = read_data(filepath)
    return df.head(), df.tail()

def data_metrics_and_visualise(filepath: str, s: Optional[str] = None):
    import matplotlib.pyplot as plt
    df = read_data(filepath)
    numeric_df = df.select_dtypes(include=[np.number])
    mat = numeric_df.to_numpy().T

    if s == "all_numeric_data":
        for row in mat:
            plt.boxplot(row)
            plt.title("Boxplot")
            plt.show()

        for row in mat:
            plt.hist(row, bins=30)
            plt.title("Histogram")
            plt.show()

    df.info()
    return df.describe(), df.head(), df.corr(), df.median(), df.mode()

