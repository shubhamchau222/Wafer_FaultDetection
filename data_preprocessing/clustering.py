from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from kneed import KneeLocator
from file_operations import file_methods

class kmeansClustering :
    """
        Method : This methods help us to cluster the training dataset
        :return : Number of cluster
        Lib uses : sklearn  , knee locator

    """
    def __init__(self ,file_object , logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def raw(self):
        pass

    def ElbowPlot( self , data ):
        ''' Method : ElbowPlot
            Description : try to apply k-means clustering and plot cluster(elbow plot)
                            and find_out the optimal number of clusters using knee locator
            fig : elbow_plot saved in dir preprocessing_data
        :param data:
        :return: self.kneed.knee Number of cluster formed
        '''
        self.data = data

        try :
            self.logger_object.log(self.file_object, 'Entered the elbow_plot method of the KMeansClustering class')
            wcss = []         #inetrtia
            for i in range(1,11):
                kmeans = KMeans(n_clusters=i,init='k-means++',random_state= 42)
                kmeans.fit(self.data)      # fitting the data into the algo
                wcss.append(kmeans.inertia_)

            a = [x for x in range(1,11)]
            # plot the curve inertia_ vs number of cluster+
            plt.plot(a,wcss)
            plt.title("The ELbow MEthod")
            plt.xlabel('Number of Clusters')
            plt.ylabel('Inertia_ (wcss)')
            #plt.show()
            plt.savefig('preprocessing_data/K-Means_Elbow.PNG')  # saving the elbow plot locally

            # finding the knee
            self.kneed = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
            self.logger_object.log(self.file_object, 'The optimum number of clusters is: ' + str(self.kneed.knee) )
            return  self.kneed.knee

        except Exception as e:
            self.logger_object.log(self.file_object, 'Finding The optimum number of clusters is: FAILED ')
            self.logger_object.log(self.file_object, 'Error:' + str(e))
            raise Exception()


    def create_clusters(self , data , number_of_clusters):
        '''
             Method : create_clusters
             Desc :  Create the clusters by taking the o/p of Elbow_plot() methods

            :param data: pandas dataFrame
            :param number_of_clusters:  kneed.knee
            :``return:
        '''
        self.logger_object.log(self.file_object ,"Entered in to Create Cluster  MEthod of the K-meansclustering class")
        self.data = data
        try :
            self.k_means = KMeans(n_clusters=number_of_clusters , init='k-means++' , random_state = 42 )
            self.k_means.fit(self.data)
            self.y_kmean = self.k_means.predict(self.data)
            self.logger_object.log(self.file_object ,"Training data clustered Successfully....")

            # file operations
            self.file_op = file_methods.File_Operation(self.file_object,self.logger_object) # initializing the file_methods
            self.save_model = self.file_op.save_model(self.k_means ,"Kmeans")  # saving the model to model dir
            self.logger_object.log(self.file_object ," Clustering Model Saved Successfully to model dir")

            self.data['Cluster'] = self.y_kmean  #creating the seperate cluster label column to dataset
            self.logger_object.log(self.file_object, 'succesfully created ' + str( self.kneed.knee) + 'clusters. Exited the create_clusters method of the KMeansClustering class')
            return  self.data

        except Exception as e:
            self.logger_object(self.file_object , "Error occcured in clustering Operation :Loc: craete_clusters Class")
            self.logger_object(self.file_object , "Error : Exception:e :: " + str(e))
            raise  Exception()















