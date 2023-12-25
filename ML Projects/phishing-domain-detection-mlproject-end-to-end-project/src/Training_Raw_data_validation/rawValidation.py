from datetime import datetime
from os import listdir
from src.application_logging.logger import App_Logger
import json
import shutil
import pandas as pd

class Raw_Data_validation:

    """
             This class shall be used for handling all the validation done on the Raw Training Data!!.

             Written By: Saurabh Naik
             Version: 1.0
             Revisions: None

             """

    def __init__(self,path):
        self.Batch_Directory = path
        self.schema_path = 'schema_training.json'
        self.logger = App_Logger()

    def valuesFromSchema(self):
        """
                        Method Name: valuesFromSchema
                        Description: This method extracts all the relevant information from the pre-defined "Schema" file.
                        Output: column_names, Number of Columns
                        On Failure: Raise ValueError,KeyError,Exception

                        Written By: Saurabh Naik
                        Version: 1.0
                        Revisions: None

        """
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            column_names = dic['ColName']
            NumberofColumns = dic['NumberofColumns']
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            message ="NumberofColumns:: %s" % NumberofColumns + "\n"
            self.logger.log(file,message)
            file.close()
        except ValueError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file,"ValueError:Value not found inside schema_training.json")
            file.close()
            raise ValueError
        except KeyError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, "KeyError:Key value error incorrect key passed")
            file.close()
            raise KeyError
        except Exception as e:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e
        return column_names, NumberofColumns

    def validateColumnLength(self,NumberofColumns):
        """
                          Method Name: validateColumnLength
                          Description: This function validates the number of columns in the csv files.
                                       It is should be same as given in the schema file.
                                       If not same file is not suitable for processing and thus is moved to Bad Raw Data folder.
                                       If the column number matches, file is kept in Good Raw Data for processing.
                          Output: None
                          On Failure: Exception

                           Written By: Saurabh Naik
                          Version: 1.0
                          Revisions: None

        """
        try:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f,"Column Length Validation Started!!")
            path = "../data/raw"
            for file in listdir(path):
                csv = pd.read_csv("../data/raw/" + file)
                if csv.shape[1] == NumberofColumns:
                    shutil.move("../data/raw/" + file, "../data/good_raw/")
                else:
                    shutil.move("../data/raw/" + file, "../data/bad_raw/")
                    self.logger.log(f, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
            self.logger.log(f, "Column Length Validation Completed!!")
        except OSError:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occured:: %s" % e)
            f.close()
            raise e
        f.close()

    def validateMissingValuesInWholeColumn(self):
        """
                                  Method Name: validateMissingValuesInWholeColumn
                                  Description: This function validates if any column in the csv file has all values missing.
                                               If all the values are missing, the file is not suitable for processing.
                                               SUch files are moved to bad raw data.
                                  Output: None
                                  On Failure: Exception

                                   Written By: Saurabh Naik
                                  Version: 1.0
                                  Revisions: None

                              """
        try:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f,"Missing Values Validation Started!!")
            path = "../data/good_raw"
            for file in listdir(path):
                csv = pd.read_csv("../data/good_raw/" + file)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count+=1
                        shutil.move("../data/good_raw/" + file, "../data/bad_raw/")
                        self.logger.log(f,"Atleast one column has empty fields !! File moved to Bad Raw Folder :: %s" % file)
                        break
                if count==0:
                    self.logger.log(f,"Every Column has atleast one non empty field !! File kept in Good Raw Folder :: %s" % file)
        except OSError:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f, "Error Occured:: %s" % e)
            f.close()
            raise e
        f.close()