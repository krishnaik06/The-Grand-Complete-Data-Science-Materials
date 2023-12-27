import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline


from src.exception import CustomException
from src.logger import logging
from src.utils import DropNaTransformer, DateTransformTransformer, FillnaTransformer, ReplaceValueTransformer, save_object
import os
from src.utils import save_object


@dataclass
class DataTransformationRecommendConfig:
    preprocessor_obj_file_path = os.path.join(
        "artifacts", "recommend_data.csv")


class DataTransformationRecommend:
    def __init__(self):
        self.data_transformation_config = DataTransformationRecommendConfig()

    def get_data_transformer_object(self, data):
        '''
        This is data transformation function
        '''
        try:

            preprocessor = Pipeline(
                steps=[('replace', ReplaceValueTransformer(9, np.nan)),
                       ('replace2', ReplaceValueTransformer("9", np.nan)),
                       ('dropna', DropNaTransformer(
                           subset=["exactPrice", "RentOrSale", "URLs"])),
                       ('date_transform', DateTransformTransformer(
                        date_column='postedOn')),
                       ('fill_na', FillnaTransformer(
                        columns=data.columns, value="Missing")),

                       ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation_recommend(self):
        try:
            Data_path = "artifact/Dataset.csv"
            Dataset = pd.read_csv(Data_path)

            logging.info("Reading preprocessor object")

            preprocessing_obj = self.get_data_transformer_object(Dataset)

            data = preprocessing_obj.fit_transform(
                Dataset)

            logging.info(f"Saved preprocessed object. {data.head()}")
            logging.info(f"saving processor : {preprocessing_obj}")

            # Saving the file just to see if processed data is valid for model training
            dataset = pd.DataFrame(data)

            # save the dataframe as a csv file
            dataset.to_csv(
                "artifacts/data_preprocessed_recommend.csv", index=False)

            combined_fea = dataset["propertyType"] + "   " + dataset["locality"] + "   " + dataset["furnishing"] + "   " + dataset["city"] + \
                "   " + dataset["bedrooms"].astype("str") + "   " + dataset["bathrooms"].astype(
                    "str") + "   " + dataset["RentOrSale"]

            combined_fea_df = pd.DataFrame({"text": combined_fea, "propertyType": dataset["propertyType"], "locality": dataset[
                                           "locality"], "furnishing": dataset["furnishing"], "city": dataset["city"], "RentOrSale": dataset["RentOrSale"], "BHK": dataset["bedrooms"], "URLs": dataset["URLs"]})

            combined_fea_df.to_csv('artifacts/recommend_data.csv', index=False)

            logging.info(
                f"Saved preprocessed data for recommendation {combined_fea_df.head()}")

            return (
                combined_fea_df,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    data_transform = DataTransformationRecommend()

    data, _ = data_transform.initiate_data_transformation_recommend()
    print(data)
