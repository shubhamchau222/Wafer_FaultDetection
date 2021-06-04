from data_ingestion import data_loader
from application_logging import logging
from data_preprocessing import clustering
from data_preprocessing import preprocessing
from best_model_finder import  tuner
from file_operations import file_methods
from sklearn.model_selection import train_test_split

class train_model:
    def __init__(self):
        self.logger_object = logging.logger_app()
        self.file_object = open('Training_Logs/model_training_logs.txt' , "a+")

    def trainingModel(self):

        self.logger_object.log(self.file_object , "Entered in Training Model Method Scuccessfully....cls:train_model")
        try:
            data_getter = data_loader.Data_Getter(self.file_object , self.logger_object)
            data = data_getter.get_data()
            #X = data.drop("Output" ,axis=1)
            #y = data['Output']

            ''' doing data preprocessing'''
            preprocessor=  preprocessing.Preprocessor(self.file_object ,self.logger_object)
            data  =  preprocessor.remove_column(data , ['Wafer'])

            # create the x and y
            X , Y = preprocessor.separate_label_feature(data , label_column_name = 'Output')
            # check is null present
            is_null_present = preprocessor.is_null_present(X)

            # if null values are present then we need to impute it
            if (is_null_present):
                X = preprocessor.impute_missing_values(X)

            # check further which columns do not contribute to predictions
            # if the standard deviation for a column is zero, it means that the column has constant values
            # and they are giving the same output both for good and bad sensors
            # prepare the list of such columns to drop

            cols_to_drop = preprocessor.get_columns_with_zero_std_deviation(X)
            # drop the the cols which aren't required
            X = preprocessor.remove_column(X , cols_to_drop)

            ''' Now we apply clustering (Divide data into number of groups)'''

            kmean = clustering.kmeansClustering(self.file_object , self.logger_object)
            number_of_clusters = kmean.ElbowPlot(X)

            # create the clusters
            X = kmean.create_clusters(X , number_of_clusters)

            X['Labels'] = Y

            list_of_clusters = X['Cluster'].unique()
            """parsing all the clusters and looking for the best ML algorithm to fit on individual cluster"""

            for i in list_of_clusters:
                cluster_data = X[X['Cluster'] == i]  # filter the data for one cluster

                # Prepare the feature and Label columns
                cluster_features = cluster_data.drop(['Labels', 'Cluster'], axis=1)
                cluster_label = cluster_data['Labels']
                # splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1 / 3 , random_state=355)
                model_finder = tuner.Model_Finder(self.file_object, self.logger_object)  # object initialization
                best_model_name , best_model = model_finder.get_best_model(x_train,y_train,x_test,y_test)

                # saving the best model to dir
                file_op = file_methods.File_Operation(self.file_object, self.logger_object)
                save_model = file_op.save_model(best_model, best_model_name + str(i))

            self.logger_object.log(self.file_object , "Model created Successfully..")
            self.logger_object.log(self.file_object , "Training COmpleted Scuccessfully , model saved in dir : models /")
            self.file_object.close()
        except Exception as e:
            self.logger_object.log(self.file_object, "Error Occured in class train model...")
            self.logger_object.log(self.file_object, "Error : " + str(e))
            self.file_object.close()
            raise Exception()



