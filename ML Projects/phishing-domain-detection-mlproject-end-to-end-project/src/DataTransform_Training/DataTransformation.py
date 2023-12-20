import os
from datetime import datetime
from os import listdir

import pandas
import pandas as pd
from src.application_logging.logger import App_Logger

class dataTransform:
     """
               This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.
               Written By: Saurabh Naik
               Version: 1.0
               Revisions: None
     """

     def __init__(self):
            self.goodDataPath = "../data/good_raw"
            self.logger = App_Logger()

     def addQuotesToStringValuesInColumn(self):
          """
                                           Method Name: addQuotesToStringValuesInColumn
                                           Description: This method converts all the columns with string datatype such that
                                                       each value for that column is enclosed in quotes. This is done
                                                       to avoid the error while inserting string values in table as varchar.
                                           Written By: Saurabh Naik
                                           Version: 1.0
                                           Revisions: None
          """
          log_file = open("Training_Logs/dataTransformLog.txt", 'a+')
          try:
               onlyfiles = [f for f in listdir(self.goodDataPath)]
               for file in onlyfiles:
                    data = pd.read_csv(self.goodDataPath+"/" + file)
                    for column in data.columns:
                         count = data[column][data[column] == '?'].count()
                         if count != 0:
                              data[column] = data[column].replace('?', "'?'")
                    data.to_csv(self.goodDataPath+ "/" + file, index=None, header=True)
                    self.logger.log(log_file," %s: Quotes added successfully!!" % file)
          except Exception as e:
               self.logger.log(log_file, "Data Transformation failed because:: %s" % e)
               log_file.close()
          log_file.close()

     def replaceMissingWithNull(self):
          """
                                           Method Name: replaceMissingWithNull
                                           Description: This method replaces the missing values in columns with "NULL" to
                                                        store in the table. We are using substring in the first column to
                                                        keep only "Integer" data for ease up the loading.
                                                        This column is anyways going to be removed during training.

                                            Written By: iNeuron Intelligence
                                           Version: 1.0
                                           Revisions: None

          """
          log_file = open("Training_Logs/dataTransformLog.txt", 'a+')
          try:
               onlyfiles = [f for f in listdir(self.goodDataPath)]
               for file in onlyfiles:
                    csv = pandas.read_csv(self.goodDataPath + "/" + file)
                    csv.fillna('NULL', inplace=True)
                    self.logger.log(log_file, " %s: Missing values replaced by Null values Successfully!!" % file)
          except Exception as e:
               self.logger.log(log_file, "Replacing missing Values failed because:: %s" % e)
               log_file.close()
          log_file.close()
