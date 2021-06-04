import pandas as pd
from sklearn.impute import KNNImputer
import numpy as np

class Preprocessor:

    '''
            Mehtod : Preprocessor
            Description : This class should be use to clean the data ,
                            separate x , y labels ,
                            impute the missing values  ,
                            give the info of any column having 0 std dev (constant/same values)


        '''
    def __init__( self , file_object , logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def remove_column(self , data , columns):
        '''
            Method : remove_column
            Description :  this method helps to remove any specific columns..
            :param data: pandas dataframe
            :param columns:[column which have to remove]
            :return: self.useful_data ( in pandas dataframe)
        '''
        self.data = data
        self.columns = columns
        self.logger_object.log(self.file_object, '\n')
        self.logger_object.log(self.file_object , 'Entered the remove_columns method of the Preprocessor class')
        try:
            self.useful_data = self.data.drop(labels=self.columns, axis=1)  # drop the given columns
            self.logger_object.log(self.file_object, 'Column Removal Successfull...')
            return self.useful_data
        except Exception as e :
            self.logger_object.log(self.file_object, 'Column Removal Fails...')
            self.logger_object.log(self.file_object, 'Exception occured in remove_columns method of the Preprocessor class. Exception message:  ' + str(e))
            raise e

    def separate_label_feature(self , data ,label_column_name ):
        self.logger_object.log(self.file_object , "Entered in  Seperate_Label_feature class Successfully...")
        try:
            self.X = data.drop(labels = label_column_name , axis=1)  # drop the columns specified and separate the feature columns
            self.Y = data[label_column_name]
            self.logger_object.log(self.file_object, "LAbels Seperated  Successfully...")
            return  self.X ,  self.Y
        except Exception as e:
            self.logger_object.log(self.file_object, "Error:" + str(e))
            self.logger_object.log(self.file_object, "LAbels Seperation Fails")

    def is_null_present(self, data):
        """
                                Method Name: is_null_present
                                Description: This method checks whether there are null values present in the pandas Dataframe or not.
                                Output: Returns a Boolean Value. True if null values are present in the DataFrame, False if they are not present.
                                On Failure: Raise Exception

                        """
        self.logger_object.log(self.file_object, 'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False
        try:
            self.null_counts = data.isna().sum()  # check for the count of null values per column
            for i in self.null_counts:
                if i > 0:
                    self.null_present = True
                    break
            if (self.null_present):  # write the logs to see which columns have null values
                dataframe_with_null = pd.DataFrame()
                dataframe_with_null['columns'] = data.columns
                dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                dataframe_with_null.to_csv('preprocessing_data/null_values.csv')  # storing the null column information to file
            self.logger_object.log(self.file_object, 'Finding missing values is a success.Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            return self.null_present
        except Exception as e:
            self.logger_object.log(self.file_object , 'Exception occured in is_null_present method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object , 'Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
            raise Exception()

    def impute_missing_values(self, data):
        """
            Method Name: impute_missing_values
            Description: This method replaces all the missing values in the Dataframe using KNN Imputer.
            Output: A Dataframe which has all the missing values imputed.
            On Failure: Raise Exception

         """
        self.logger_object.log(self.file_object, 'Entered the impute_missing_values method of the Preprocessor class')
        self.data = data
        try:
            imputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values=np.nan)
            self.new_array = imputer.fit_transform(self.data)  # impute the missing values
            # convert the nd-array returned in the step above to a Dataframe
            self.new_data = pd.DataFrame(data=self.new_array, columns=self.data.columns)
            self.logger_object.log(self.file_object,
                                   'Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            return self.new_data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            raise Exception()

    def get_columns_with_zero_std_deviation(self, data):

        """
            Method Name: get_columns_with_zero_std_deviation
            Description: This method finds out the columns which have a standard deviation of zero.
            Output: List of the columns with standard deviation of zero
            On Failure: Raise Exception
        """
        self.logger_object.log(self.file_object , 'Entered the get_columns_with_zero_std_deviation method of the Preprocessor class')
        self.columns = data.columns
        self.data_n = data.describe()
        self.col_to_drop = []
        try:
            for x in self.columns:
                if (self.data_n[x]['std'] == 0):  # check if standard deviation is zero
                    self.col_to_drop.append(x)  # prepare the list of columns with standard deviation zero
            self.logger_object.log(self.file_object,
                                   'Column search for Standard Deviation of Zero Successful. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            return self.col_to_drop

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_columns_with_zero_std_deviation method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Column search for Standard Deviation of Zero Failed. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            raise Exception()









