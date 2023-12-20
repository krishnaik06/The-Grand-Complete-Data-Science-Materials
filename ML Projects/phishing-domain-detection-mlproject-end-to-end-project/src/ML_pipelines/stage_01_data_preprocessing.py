from pathlib import Path
import argparse
from src.utils.common_utils import read_params, clean_prev_dirs_if_exists, create_dir,correlation
import pandas as pd
from src.application_logging.logger import App_Logger
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import StandardScaler


def data_preprocessing(config_path):
    """
                    Method Name: data_preprocessing
                    Description: This method performs data preprocessing by reading parameters from param.yaml and then
                    pereforming feature engineering and feature selection based on EDA given in Jupyter notebook
                    notebooks/EDA and preprocessing.
                    Output: Return a preprocessed csv having the data ready for ML algos
                    On Failure: Raise Error

                     Written By: Saurabh Naik
                    Version: 1.0
                    Revisions: None

                    """
    try:

        # Initializing Logger object
        logger = App_Logger()
        p = Path(__file__).parents[2]
        path=str(p)+"/src/Training_Logs/DataPreprocessingLog.txt"
        file = open(path, "a+")
        logger.log(file, "Data preprocessing started ")

        # Reading of params from params.yaml file
        config = read_params(config_path)
        data_path = config["data_source"]["data_source"]
        preprocessed_dir = config["preprocessed_data"]["preprocessed_dir"]
        train_data_path = config["preprocessed_data"]["train_data"]
        test_data_path = config["preprocessed_data"]["test_data"]
        target_col=config["base"]["target_col"]
        random_state = config["base"]["random_state"]
        sampling_strategy = config["base"]["sampling_strategy"]
        test_size=config["base"]["test_size"]

        #Getting dataframe from the csv provided by Database
        p = Path(__file__).parents[2]
        path = str(p)+str(data_path)
        df = pd.read_csv(path)
        logger.log(file, "Data reading Started...")

        #Splitting test and train data to avoid data leakage
        X = df.drop(labels=target_col, axis=1)
        Y = df[[target_col]]
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=random_state)
        logger.log(file, "Data split to avoid data leakage")

        #Feature Engineering
        logger.log(file, "Feature Engineering Started...")

        #Feature Engineering: Handling imbalanced dataset.
        logger.log(file, "Handling imbalanced dataset.")
        sm = SMOTE(sampling_strategy=sampling_strategy, random_state=random_state)
        # Fit the model to generate the data.
        oversampled_X_train, oversampled_Y_train = sm.fit_resample(X_train, y_train)
        train_data = pd.concat([pd.DataFrame(oversampled_Y_train), pd.DataFrame(oversampled_X_train)], axis=1)
        oversampled_X_test, oversampled_Y_test = sm.fit_resample(X_test, y_test)
        test_data = pd.concat([pd.DataFrame(oversampled_Y_test), pd.DataFrame(oversampled_X_test)], axis=1)
        logger.log(file, "Imbalanced Dataset handled by SMOTE")

        #Feature Engineering: Handling outliers in all features dataset of train data.
        logger.log(file, "Handling outliers in all features of training dataset.")
        for feature in train_data.columns:
            IQR = train_data[feature].quantile(0.75) - train_data[feature].quantile(0.25)
            lower_bridge = train_data[feature].quantile(0.25) - (IQR * 1.5)
            upper_bridge = train_data[feature].quantile(0.75) + (IQR * 1.5)
            train_data.loc[train_data[feature] < lower_bridge, feature] = lower_bridge
            train_data.loc[train_data[feature] >= upper_bridge, feature] = upper_bridge
        logger.log(file, "Outliers have been handled in training data")

        # Feature Engineering: Handling outliers in all features dataset of test data.
        logger.log(file, "Handling outliers in all features of test dataset.")
        for feature in test_data.columns:
            IQR = test_data[feature].quantile(0.75) - test_data[feature].quantile(0.25)
            lower_bridge = test_data[feature].quantile(0.25) - (IQR * 1.5)
            upper_bridge = test_data[feature].quantile(0.75) + (IQR * 1.5)
            test_data.loc[test_data[feature] < lower_bridge, feature] = lower_bridge
            test_data.loc[test_data[feature] >= upper_bridge, feature] = upper_bridge
        logger.log(file, "Outliers have been handled in test data")

        # Feature Selection
        logger.log(file, "Feature Selection Started...")
        X_train = train_data.drop(labels=target_col, axis=1)
        Y_train = train_data[[target_col]]
        X_test = test_data.drop(labels=target_col, axis=1)
        Y_test = test_data[[target_col]]

        #Feature selection:Finding correlated features and removing those features which are 85% correlated in training data
        corr_features = correlation(X_train, 0.85)

        #Removing correlated features from training data
        X_train.drop(corr_features,axis=1,inplace=True)
        logger.log(file, "Removed correlated features from training data")

        # Feature selection:Finding correlated features and removing those features which are 85% correlated in test data
        corr_features = correlation(X_test, 0.85)

        # Removing correlated features from test data
        X_test.drop(corr_features,axis=1,inplace=True)
        logger.log(file, "Removed correlated features from test data")

        # Finding features having 0 varience in  training data
        var_thres = VarianceThreshold(threshold=0)
        var_thres.fit(X_train)
        constant_columns = [column for column in X_train.columns
                            if column not in X_train.columns[var_thres.get_support()]]

        #dropping features having 0 varience from train data
        X_train.drop(constant_columns, axis=1, inplace=True)
        logger.log(file, "Removed features having 0 varience from training data")

        # Finding features having 0 varience in  test data
        var_thres = VarianceThreshold(threshold=0)
        var_thres.fit(X_test)
        constant_columns = [column for column in X_test.columns
                            if column not in X_test.columns[var_thres.get_support()]]

        # dropping features having 0 varience from test data
        X_test.drop(constant_columns,axis=1,inplace=True)
        logger.log(file, "Removed features having 0 varience from test data")

        #creating new test and train dataframe
        df_final_train = pd.DataFrame(X_train)
        df_final_test = pd.DataFrame(X_test)

        #Applying Standard scaling on X data of train and test data
        scaled_features_train = StandardScaler().fit_transform(df_final_train.values)
        scaled_features_test = StandardScaler().fit_transform(df_final_test.values)
        scaled_features_df_train = pd.DataFrame(scaled_features_train, index=df_final_train.index,
                                                columns=df_final_train.columns)
        scaled_features_df_test = pd.DataFrame(scaled_features_test, index=df_final_test.index,
                                               columns=df_final_test.columns)

        # Adding target column on scaled X data of train and test dataframes
        scaled_features_df_train[target_col] = pd.DataFrame(Y_train)
        scaled_features_df_test[target_col] = pd.DataFrame(Y_test)
        logger.log(file, "Feature Selection Completed")

        #Creating a new directory preprocessed inside Data and inserting preprocessed df in csv file
        clean_prev_dirs_if_exists(preprocessed_dir)
        create_dir(dirs=[preprocessed_dir])
        p = Path(__file__).parents[2]
        path = str(p) + str(train_data_path)
        scaled_features_df_train.to_csv(path, index=False)
        path = str(p) + str(test_data_path)
        scaled_features_df_test.to_csv(path, index=False)
        logger.log(file, "Data preprocessing completed")

    except Exception as e:
        logger = App_Logger()
        p = Path(__file__).parents[2]
        path = str(p) + "/src/Training_Logs/DataPreprocessingLog.txt"
        file = open(path, "a+")
        logger.log(file, "error encountered due to: %s" %e)
        raise e


if __name__ == '__main__':
    p = Path(__file__).parents[2]
    path=str(p) + "\params.yaml"
    args = argparse.ArgumentParser()
    args.add_argument("--config", default=path)
    parsed_args = args.parse_args()

    try:

        data = data_preprocessing(config_path=parsed_args.config)
    except Exception as e:
        raise e
