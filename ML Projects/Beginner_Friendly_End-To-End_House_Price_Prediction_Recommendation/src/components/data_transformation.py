import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import DropNaTransformer, DateTransformTransformer, FillnaTransformer, CategoricalLabelTransformer, ReplaceValueTransformer, save_object
import os
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This is data transformation function
        '''
        try:
            categorical_col = ['propertyType',
                               'locality',
                               'furnishing',
                               'city',
                               'bedrooms',
                               'bathrooms',
                               'RentOrSale',
                               'exactPrice',
                               ]
            # Creating the initial pipeline

            imp_feature = ['propertyType',
                           'locality',
                           'furnishing',
                           'city',
                           'bedrooms',
                           'bathrooms',
                           'RentOrSale',
                           "exactPrice"]

            Initial_pipline = Pipeline(
                steps=[('replace', ReplaceValueTransformer(9, np.nan)),
                       ('replace2', ReplaceValueTransformer("9", np.nan)),
                       ('dropna', DropNaTransformer(subset=["exactPrice"])),
                       #    ('date_transform', DateTransformTransformer(
                       #     date_column='postedOn')),
                       ('fill_na', FillnaTransformer(
                        columns=imp_feature, value="Missing")),
                       ('categorical_label_transform',
                           CategoricalLabelTransformer(categorical_col)),

                       ]
            )

            logging.info(f"Imp features : {imp_feature}")
            logging.info(f"categorical_col : {categorical_col}")

            preprocessor = ColumnTransformer(
                [
                    ("Initial_pipeline", Initial_pipline, imp_feature),
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, raw_data_path):
        try:
            dataset = pd.read_csv(raw_data_path)

            logging.info(f"Read raw data path {raw_data_path}")
            logging.info("Reading preprocessor object")

            preprocessing_obj = self.get_data_transformer_object()

            # logging.info(f"dataset columns : {dataset.columns}")
            Input_fea = ['propertyType',
                         'locality',
                         'furnishing',
                         'city',
                         'bedrooms',
                         'bathrooms',
                         'RentOrSale',
                         "exactPrice"]

            data = preprocessing_obj.fit_transform(
                dataset[Input_fea])

            # logging.info(f"Saved preprocessing object. {data}")
            logging.info(f"saving processor : {preprocessing_obj}")

            # Saving the file just to see if processed data is valid for model training
            DF = pd.DataFrame(data, columns=Input_fea)

            # save the dataframe as a csv file
            DF.to_csv("artifacts/processed_data.csv", index=False)

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                DF,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
