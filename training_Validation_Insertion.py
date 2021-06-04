from Training_Raw_data_validation.rawValidation import Raw_Data_validation
from DataTypeValidation_Insertion_Training.DataTypeValidation import dBOperation
from DataTransform_Training.DataTransformation import DataTransformation
from application_logging.logging  import logger_app


class train_validation:
    def __init__(self , path ):
        self.dataTransformation = DataTransformation()
        self.logger = logger_app()
        self.DBoperation = dBOperation()
        self.raw_data = Raw_Data_validation(path)
        self.training_log_fileObj = open("Training_Logs/Training_Main_Log.txt" , "a+")

    def train_validation(self):
        try:
            self.logger.log(self.training_log_fileObj , "Training Validation Started....")
            #readinfg the training validation schema
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = self.raw_data.valuesFromSchema()
            # creating regx
            regex = self.raw_data.manualRegexCreation()

            #validating the Training File names
            self.raw_data.validationFileNameRaw(regex ,LengthOfDateStampInFile , LengthOfTimeStampInFile )

            # validating column length in the file
            self.raw_data.validateColumnLength(noofcolumns)

            # validating if any column has all values missing
            self.raw_data.validateMissingValuesInWholeColumn()
            self.logger.log(self.training_log_fileObj  ,  "Raw Data Validation Complete....")

            self.logger.log(self.training_log_fileObj, "Starting Data Transforamtion!!")
            # replacing blanks in the csv file with "Null" values to insert in table
            self.dataTransformation.replaceMissingWithNull()
            self.logger.log(self.training_log_fileObj, "DataTransformation Completed!!!")

            self.logger.log(self.training_log_fileObj , "Creating Training_Database and tables on the basis of given schema!!!")

            # create database with given name, if present open the connection! Create table with columns given in schema
            self.DBoperation.createTableDb("Training" , column_names )
            self.logger.log(self.training_log_fileObj , "Table creation Completed!!")
            self.logger.log(self.training_log_fileObj , "Insertion of Data into Table started!!!!")

            # insert csv files in the table
            self.DBoperation.insertIntoTableGoodData('Training')
            self.logger.log(self.training_log_fileObj, "Insertion in Table completed!!!")
            self.logger.log(self.training_log_fileObj, "Deleting Good Data Folder!!!")

            # Delete the good data folder after loading files in table
            self.raw_data.deleteExistingGoodDataTrainingFolder()
            self.logger.log(self.training_log_fileObj, "Good_Data folder deleted!!!")
            self.logger.log(self.training_log_fileObj, "Moving bad files to Archive and deleting Bad_Data folder!!!")

            # Move the bad files to archive folder
            self.raw_data.moveBadFilesToArchiveBad()
            self.logger.log(self.training_log_fileObj, "Bad data moved moveBadFilesToArchiveBad....Bad folder Deleted!!")

            self.logger.log(self.training_log_fileObj, "Training Validation Completed....")
            self.logger.log(self.training_log_fileObj, "Extracting Csv File From Table..!!")
            self.DBoperation.selectingDatafromtableintocsv('Training')
            self.logger.log(self.training_log_fileObj, "Csv data Extracted successfully from the table...!!")

            # close the loggeing file obj
            self.training_log_fileObj.close()

        except Exception as e :
            self.logger.log(self.training_log_fileObj , "%s " %e)
            raise e




























