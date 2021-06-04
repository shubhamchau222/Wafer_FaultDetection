# file ddescription : This class is for the database operation
# create the database connection and create tables , import raw good / bad data from good data directory

import os
import shutil
import sqlite3
import csv
from application_logging.logging import logger_app
from datetime import datetime


class dBOperation:
    def __init__(self):
        self.path = 'Training_Database/'
        self.badFilePath = "Training_Raw_files_validated/Bad_Raw"
        self.goodFilePath = "Training_Raw_files_validated/Good_Raw"
        self.logger = logger_app()

    def dataBaseConnection(self ,DatabaseName):
        '''
                    Method : dataBaseCreation
                    Description: This method create the database , if database already Exist
                                then it's make connection to the that database
                    Output: Connection to the DB
                    On Failure: Raise ConnectionError
        '''
        try:
            conn = sqlite3.connect(self.path + DatabaseName + '.db')
            log_file = open("Training_Logs/DataBaseConnectionLog.txt" , "a+")
            massage = "Opened %s database successfully" % DatabaseName
            self.logger.log(log_file , massage)
            log_file.close()
        except ConnectionError :
            log_file = open("Training_Logs/DataBaseConnectionLog.txt" , "a+")
            massage = "Error while connecting to database: %s" %ConnectionError
            self.logger.log(log_file , massage)
            log_file.close()
            raise ConnectionError

        return conn

    def createTableDb(self, DatabaseName, column_names):
        """
            Method : createTableDb
            Description : this method use to store the good raw data in given database ,
                            after training Raw Data validation ..
            ON_Failure : raise Exception

        """
        try :
            conn = self.dataBaseConnection(DatabaseName)
            c = conn.cursor()
            c.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'")
            if c.fetchone()[0] == 1:
                conn.close()
                log_file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(log_file, "Tables created successfully!!")
                log_file.close()

                logg_file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(logg_file, "Closed %s database successfully" % DatabaseName)
                logg_file.close()
            else:
                for key in column_names.keys():
                    type = column_names[key]
                    # in try block we check if the table exists, if yes then add columns to the table
                    # else in catch block we will create the table
                    try :
                        conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key, dataType=type))
                    except :
                        conn.execute('CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))

                conn.close()

                file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()

                file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()

        except Exception as e:
            file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()
            conn.close()
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
            raise e

    def insertIntoTableGoodData(self , Database):
        '''
            MEthod : insertIntoTableGoodData
            Description : this method helps to transfer the good data from good Training data folder to
                            good data Database..


            :return: None
        '''

        goodFilePath = self.goodFilePath
        badFilePath = self.badFilePath
        only_files = [file for file in os.listdir(goodFilePath)]
        log_file = open("Training_Logs/DbInsertLog.txt" , "a+")
        conn = self.dataBaseConnection(Database)  # connect to the given database

        for file in only_files:
            try :
                with open( goodFilePath + '/'+ file , "r") as f :
                    next(f)
                    reader  = csv.reader(f ,delimiter="\n")
                    for  line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))
                                self.logger.log(log_file, " %s: File loaded successfully!!" % file)
                                conn.commit()
                            except Exception as e:
                                raise e
            except Exception as e:
                conn = self.dataBaseConnection(Database)
                conn.rollback()
                self.logger.log(log_file, "Error while creating table: %s " % e)
                shutil.move(goodFilePath + '/' + file, badFilePath)
                self.logger.log(log_file, "File Moved Successfully %s" % file)
                log_file.close()
                conn.close()

        conn.close()
        log_file.close()

    def selectingDatafromtableintocsv(self,Database):
        """
            method : selectingDatafromtableintocsv
            Description : It's collect data from database and convert data into csv format..

            :return:
        """
        self.fileFromDb = 'Training_FileFromDB/'
        self.fileName = 'InputFile.csv'
        log_file = open("Training_Logs/ExportToCsv.txt", 'a+')

        try:
            conn = self.dataBaseConnection(Database)
            sqlSelect = "SELECT *  FROM Good_Raw_Data"
            cursor = conn.cursor()
            cursor.execute(sqlSelect)

            results = cursor.fetchall()
            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            # Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)
                # Open CSV file for writing.
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''), delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.logger.log(log_file , "File Exported to csv Successfully.....")
            log_file.close()

        except Exception as e :
            self.logger.log(log_file, "File exporting failed. Error : %s" % e)
            log_file.close()








        































