import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from src.NBA_Project import logger
from src.NBA_Project.entity.config_entity import DataTransformationConfig



class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def transform_data(self):

        data=pd.read_csv(self.config.data_path)
        train,test=train_test_split(data,test_size=0.2,shuffle=True,stratify=data['TARGET_5Yrs'],random_state=42)

        num_col=list(train.drop(['TARGET_5Yrs'],axis=1).select_dtypes(include=['int64','float64']))
        for col in num_col:

                q1=train[col].quantile(0.25)
                q3=train[col].quantile(0.75)
                IQR=q3-q1
                lb=q1-1.5*IQR
                up=q3+1.5*IQR

                train=train[(train[col]>=lb) & (train[col]<=up)]

        imputer=SimpleImputer(strategy='median')

        train["3P%"]=imputer.fit_transform(train[['3P%']])
        test["3P%"]=imputer.transform(test[['3P%']])

        train.drop('Name',axis=1,inplace=True)
        test.drop('Name',axis=1,inplace=True)

        train.to_csv(os.path.join(self.config.root_dir, "train.csv"),index = False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"),index = False)

        logger.info("Splited data into training and test sets")
        logger.info(train.shape)
        logger.info(test.shape)

        print(train.shape)
        print(test.shape)


