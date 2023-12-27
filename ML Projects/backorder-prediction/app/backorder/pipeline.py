import warnings

import joblib
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')


class BackorderPredictor:
    def __init__(self):
        self.num_col_list = ['national_inv', 'lead_time', 'in_transit_qty', 'forecast_3_month', 'forecast_6_month',
                             'forecast_9_month', 'sales_1_month', 'sales_3_month', 'sales_6_month', 'sales_9_month',
                             'min_bank', 'pieces_past_due', 'perf_6_month_avg', 'perf_12_month_avg', 'local_bo_qty']
        self.best_feat = None
        self.sc = None
        self.model = None

    def _load_model_files(self):
        # Fetching the best features
        self.best_feat = joblib.load(
            'backorder/model/test_best_feat.pkl').tolist()

        # Fetching the trained standardization object instance
        self.sc = joblib.load('backorder/model/sc.pkl')

        # Fetching the trained model
        self.model = joblib.load(
            'backorder/model/backorder_best_model.pkl')

    def _encode_bool_columns(self, df_test):
        dict_map_bool = {'Yes': 1.0, 'No': 0.0}

        df_test['deck_risk'] = df_test['deck_risk'].map(dict_map_bool)
        df_test['potential_issue'] = df_test['potential_issue'].map(
            dict_map_bool)
        df_test['oe_constraint'] = df_test['oe_constraint'].map(dict_map_bool)
        df_test['ppap_risk'] = df_test['ppap_risk'].map(dict_map_bool)
        df_test['stop_auto_buy'] = df_test['stop_auto_buy'].map(dict_map_bool)
        df_test['rev_stop'] = df_test['rev_stop'].map(dict_map_bool)

        return df_test

    def _replace_performance_columns(self, df_test):
        df_test.perf_6_month_avg.replace({-99.0: np.nan}, inplace=True)
        df_test.perf_12_month_avg.replace({-99.0: np.nan}, inplace=True)
        return df_test

    def _drop_sku_col(self, df_test):
        return df_test.drop(columns=['sku'])

    def _handle_missing_values(self, df_test):
        df_test.lead_time.replace(to_replace=np.nan, value=8, inplace=True)
        df_test.perf_6_month_avg.replace(
            to_replace=np.nan, value=.85, inplace=True)
        df_test.perf_12_month_avg.replace(
            to_replace=np.nan, value=.83, inplace=True)
        return df_test

    def _perform_standardization(self, df_test):
        df_test_num_sc = self.sc.transform(df_test[self.num_col_list].values)
        df_test_num_sc = pd.DataFrame(
            df_test_num_sc, index=df_test.index, columns=self.num_col_list)
        return df_test_num_sc

    def add(self, df, num_cols):
        for i in num_cols:
            for j in num_cols:
                if i != j:
                    df[i + '_' + j + '_add'] = df[i] + df[j]
        return df

    def mult(self, df, num_cols):
        for i in num_cols:
            for j in num_cols:
                if i != j:
                    df[i + '_' + j + '_mult'] = df[i] * df[j]
        return df

    # Function to perform inverse of features
    def inv(self, df, num_cols):
        for i in num_cols:
            df[i + '_' + 'inv'] = 1 / (df[i] + 0.001)
        return df

    # Function to perform square of features
    def square(self, df, num_cols):
        for i in num_cols:
            df[i + '_' + 'square'] = df[i] * df[i]
        return df

    # Function to perform square root of features
    def sqrt(self, df, num_cols):
        for i in num_cols:
            df[i + '_' + 'square_root'] = np.sqrt(abs(df[i]))
        return df

    # Function to perform log of features
    def log(self, df, num_cols):
        for i in num_cols:
            df[i + '_' + 'log'] = (np.log(abs(df[i]) + 1))
        return df

    def perform_feature_engineering(self, df_test):
        df_test_trans = self.add(df_test, self.num_col_list)
        df_test_trans = self.mult(df_test_trans, self.num_col_list)
        df_test_trans = self.inv(df_test_trans, self.num_col_list)
        df_test_trans = self.square(df_test_trans, self.num_col_list)
        df_test_trans = self.sqrt(df_test_trans, self.num_col_list)
        df_test_trans = self.log(df_test_trans, self.num_col_list)
        return df_test_trans

    def _get_best_features(self, df_test_trans):
        df_test_final = df_test_trans[self.best_feat]
        return df_test_final

    def _get_ytest(self, df_test_trans):
        y_test = df_test_trans['went_on_backorder'].values
        return y_test

    def preprocessing(self, df_test):
        # Encode categorical columns with values Yes and No to 1 and 0 respectively
        df_test = self._encode_bool_columns(df_test)

        # Replacing -99 in performance columns with nan
        df_test = self._replace_performance_columns(df_test)

        # Dropping sku column
        df_test = self._drop_sku_col(df_test)

        # Handling missing values with median values
        df_test = self._handle_missing_values(df_test)

        # Performing Standardization
        df_test_num_sc = self._perform_standardization(df_test)

        # Assigning numerical columns to original dataframe
        for i in self.num_col_list:
            df_test[i] = df_test_num_sc[i]

        # Performing feature engineering
        df_test_trans = self.perform_feature_engineering(df_test)

        # Fetching the best features
        df_test_final = self._get_best_features(df_test_trans)

        return df_test_final

    def predict(self, df):
        df_test_final = self.preprocessing(df)
        y_pred_test = self.model.predict(df_test_final)
        y_pred_test = [int(i) for i in y_pred_test.tolist()]
        return y_pred_test
