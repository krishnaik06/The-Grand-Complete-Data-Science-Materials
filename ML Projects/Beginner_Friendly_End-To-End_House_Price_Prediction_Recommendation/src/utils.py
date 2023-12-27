import os
import sys
import datetime

import numpy as np
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

from src.exception import CustomException
from src.logger import logging


def date_transform(date):
    try:
        date_object = datetime.datetime.strptime(date, "%b %d, '%y")
        formatted_date = datetime.datetime.strftime(date_object, "%Y-%m-%d")
        new_date = datetime.datetime.strptime(
            formatted_date, "%Y-%m-%d").date()
        current_date = datetime.date.today()
        Days = (current_date - new_date).days
        return Days

    except Exception as e:
        raise CustomException(e, sys)


def remove_outliers_iqr(df):
    # Calculate the first quartile (25th percentile) and third quartile (75th percentile)
    q1 = df.quantile(0.25)
    q3 = df.quantile(0.75)

    # Calculate the interquartile range (IQR)
    iqr = q3 - q1

    # Define the lower and upper bounds for outliers
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    if lower_bound['exactPrice'] < 0:
        lower_bound = df.min()

    # Filter rows where any value is within the lower and upper bounds
    df_no_outliers = df[~((df < lower_bound) | (df > upper_bound)).any(axis=1)]

    return df_no_outliers


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            # model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        logging.info(f"utils model trainer : {report} , { model.get_params()}")
        return report

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)


class ReplaceValueTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, value, replace_with):
        self.value = value
        self.replace_with = replace_with

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_replaced = X.replace(self.value, self.replace_with)
        return X_replaced


class DropNaTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, subset):
        self.subset = subset

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_dropped = X.dropna(subset=self.subset)
        return X_dropped


class CategoricalLabelTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, categorical_features):
        # logging.info(f"Debugging- feature1 : {categorical_features}")

        if "exactPrice" in categorical_features:
            categorical_features.remove('exactPrice')
        # logging.info(f"Debugging- feature2 : {categorical_features}")
        self.categorical_features = categorical_features
        self.labels_ordered_dict = {}

    def fit(self, X, y=None):
        for feature in self.categorical_features:
            labels_ordered = X.groupby(
                [feature])['exactPrice'].mean().sort_values().index
            labels_ordered_dict = {k: i for i,
                                   k in enumerate(labels_ordered, 0)}
            self.labels_ordered_dict[feature] = labels_ordered_dict
        return self

    def transform(self, X):
        X_transformed = X.copy()
        # logging.info(f"Debugging- feature3 : {X.columns}")

        for feature in X.columns:
            if feature != 'exactPrice' and feature != 'postedOn':
                X_transformed[feature] = X_transformed[feature].map(
                    self.labels_ordered_dict[feature])
        return X_transformed


class DateTransformTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, date_column):
        self.date_column = date_column

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.copy()
        X_transformed[self.date_column] = X_transformed[self.date_column].apply(
            self.date_transform)
        return X_transformed

    @staticmethod
    def date_transform(date):
        date_object = datetime.datetime.strptime(date, "%b %d, '%y")
        formatted_date = datetime.datetime.strftime(date_object, "%Y-%m-%d")
        new_date = datetime.datetime.strptime(
            formatted_date, "%Y-%m-%d").date()
        current_date = datetime.date.today()
        ab = (current_date - new_date).days
        return ab


class FillnaTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns, value):
        self.columns = columns
        self.value = value

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.copy()
        X_transformed[self.columns] = X_transformed[self.columns].fillna(
            value=self.value)
        return X_transformed


def format_indian_currency(num, currency_symbol='₹'):
    # Convert the number to a string and reverse it for easier processing
    num_str = str(num)[::-1]

    # Create a list to store the formatted parts of the number

    formatted_parts = []

    chunk = num_str[0:3][::-1]
    formatted_parts.append(chunk)
    # Iterate through the reversed number string in chunks of three digits
    for i in range(3, len(num_str), 2):
        # Get the chunk and reverse it back to the original order
        chunk = num_str[i:i+2][::-1]
        formatted_parts.append(chunk)

    # Reverse the list to get the correct order and join the parts with commas
    formatted_number = ','.join(formatted_parts[::-1])

    # Add the currency symbol at the beginning of the formatted number
    formatted_number = f"{currency_symbol}{formatted_number}"

    return formatted_number


def output_within_range(number):
    # Calculate the output within the range of 15000 to 20000
    number1 = number/pow(10, 3)
    number1 = np.round(number1) * pow(10, 3)
    number2 = number/pow(10, 4)
    number2 = np.round(number2) * pow(10, 4)
    # Convert the output to a string and return it
    num1 = format_indian_currency(str(number1)[:-2])
    num2 = format_indian_currency(str(number2)[:-2])

    if number1 >= number2:
        output_str = f"{num2} - {num1}"
    else:

        output_str = f"{num1} - {num2}"

    print(number)
    # print(format_indian_currency(str(number1)[:-2]))
    return output_str
