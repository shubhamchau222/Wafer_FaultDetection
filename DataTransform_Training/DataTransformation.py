import os
from datetime import datetime
import pandas as pd
import csv
from application_logging.logging import logger_app

class DataTransformation:
    '''
        method : DataTransformation
        Description : This method help us to transform data before loading it into the database

    '''
    def __init__(self):
        self.logger =  logger_app()
        self.goodDataPath = "Training_Raw_files_validated/Good_Raw"

    def replaceMissingWithNull(self):
        '''
            Method Name: replaceMissingWithNull
               Description: This method replaces the missing values in columns with "NULL" to
                        store in the table. We are using substring in the first column to
                        keep only "Integer" data for ease up the loading.
                        This column is anyways going to be removed during training.
        '''
        log_file = open("Training_Logs/dataTransformLog.txt" , "a+")
        self.logger.log(log_file , "Data Transformation Started Successfully !!....")

        try:
            filenames = [x for x in os.listdir(self.goodDataPath)]
            for file in filenames:
                file_path = os.path.join(self.goodDataPath , file )
                df = pd.read_csv(file_path)
                df.fillna("NULL" , inplace = True)
                # get the wafer code only
                df['Wafer'] = df['Wafer'].str[6:]
                # export data to csv
                df.to_csv(self.goodDataPath + "/" + file   , index = None , header = True)
                self.logger.log(log_file, " %s: File Transformed successfully!!" % file)
        except Exception as e:
               self.logger.log(log_file, "Data Transformation failed because:: %s" % e)
               log_file.close()
        log_file.close()








