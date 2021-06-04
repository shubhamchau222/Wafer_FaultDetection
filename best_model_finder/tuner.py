from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics  import roc_auc_score,accuracy_score


class Model_Finder:
    '''
        This class shall  be used to find the model with best accuracy and AUC score.

    '''

    def __init__(self , file_object , logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.clf = RandomForestClassifier()
        self.xgb = XGBClassifier(objective="binary:logistic")

    def get_best_params_for_random_forest(self , x_train , y_train):
        '''   Methods : get_best_params_for_random_forest
                Description : gives the best parameters of the random forest at which we get good
                              performance and accuracy by using hyper-Parameter tuning
                              Internally applies the Grisd_search cv..

                :param x_train: preprocessed x_train data
                :param y_train: Y_train ( Binary output feature )
                :return: best parameters from
        '''
        self.logger_object.log( self.file_object , "Enterd into get_best_params_for_random_forest method successfully....cls:Model_Finder " )
        try:
            #create the parameters grid
            self.parms_grid = {"n_estimators": [10, 50,70, 100, 130], "criterion": ['gini', 'entropy'],
                               "max_depth": range(2, 4, 1), "max_features": ['auto', 'log2'] }
            # creating the object of grid class
            self.grid = GridSearchCV( estimator=self.clf ,param_grid=self.parms_grid , cv = 6  , verbose=3)
            self.grid.fit(x_train , y_train)
            self.best_params = self.grid.best_params_
            # here we get the dictionary of the best parameters
            self.criterion = self.best_params['criterion']
            self.max_depth = self.best_params['max_depth']
            self.max_features = self.best_params['max_features']
            self.n_estimators = self.best_params["n_estimators"]

            # creating the new model with the  best parameters
            self.clf  = RandomForestClassifier(n_estimators=self.n_estimators, criterion = self.criterion,
                                               max_depth=self.max_depth, max_features=self.max_features)
            self.clf.fit(x_train ,  y_train)
            # model created
            self.logger_object.log(self.file_object , " Best parameters for the RandomForest Classifire are founded...")
            self.logger_object.log(self.file_object, " Rand_F Best Params: " + str(self.best_params))
            return self.clf

        except Exception as e:
            self.logger_object.log(self.file_object , "Error occured in method get_best_params_for_random_forest , cls :Model_Finder ")
            self.logger_object.log(self.file_object , "Exception : Error :" + str(e))
            raise Exception()

    def get_best_params_for_Xgboost (self , x_train , y_train):
        '''
                Method Name: get_best_params_for_xgboost
                Description: get the parameters for XGBoost Algorithm which give the best accuracy.
                             Use Hyper Parameter Tuning.

                :param x_train:
                :param y_train:
                :return:
        '''

        try:
            self.logger_object.log(self.file_object,"Enterd into get_best_params_for_Xgboost method successfully....cls:Model_Finder ")

            # initializing with different combination of parameters
            self.param_grid_xgboost = {

                'learning_rate': [0.5, 0.1, 0.01, 0.001 ],
                'max_depth': [3,5,7, 10, 20],
                'n_estimators': [10, 50, 100, 200]

                }
            # Creating an object of the Grid Search class
            self.grid = GridSearchCV(self.xgb, self.param_grid_xgboost, verbose=3 , cv=5 )
            # finding the best parameters
            self.grid.fit(x_train, y_train)

            # extracting the best parameters
            self.best_params = self.grid.best_params_
            self.learning_rate = self.best_params['learning_rate']
            self.max_depth = self.best_params['max_depth']
            self.n_estimators = self.best_params['n_estimators']

            self.xgb = XGBClassifier( learning_rate=self.learning_rate, max_depth=self.max_depth,
                                     n_estimators=self.n_estimators)
            # training the mew model
            self.xgb.fit(x_train, y_train)
            self.logger_object.log(self.file_object, " Best parameters for the XGBoost Classifier are founded...")
            self.logger_object.log(self.file_object, " XGBoost Classifier Params: " + str( self.best_params))
            return self.xgb

        except Exception as e:
            self.logger_object.log(self.file_object, "Error occured in method : get_best_params_for_Xgboost , cls :Model_Finder ")
            self.logger_object.log(self.file_object, "Exception : Error :" + str(e))
            raise Exception()

    def get_best_model(self,x_train,y_train,x_test,y_test):
        '''
                Method Name: get_best_model
                Description: Find out the Model which has the best AUC score.
                Output: The best model name and the model object
                On Failure: Raise Exception

                :return: best model
        '''

        self.logger_object.log(self.file_object , 'Entered the get_best_model method of the Model_Finder class')
        # create best model for XGBoost
        try:
            self.xgboost = self.get_best_params_for_Xgboost(x_train, y_train)
            self.prediction_xgboost = self.xgboost.predict(x_test)  # Predictions using the XGBoost Model

            #if len(y_test.unique()) == 1:  # if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
            self.xgboost_score = accuracy_score(y_test, self.prediction_xgboost)
            self.logger_object.log(self.file_object, 'Accuracy for XGBoost:' + str(self.xgboost_score))  # Log AUC
            #else:
            self.xgboost_score = roc_auc_score(y_test, self.prediction_xgboost)  # AUC for XGBoost
            self.logger_object.log(self.file_object, 'AUC for XGBoost:' + str(self.xgboost_score))  # Log AUC

            # create best model for Random Forest
            self.random_forest = self.get_best_params_for_random_forest(x_train, y_train)
            self.prediction_random_forest = self.random_forest.predict(x_test)  # prediction using the Random Forest Algorithm

            #if len( y_test.unique()) == 1:  # if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
            self.random_forest_score = accuracy_score(y_test, self.prediction_random_forest)
            self.logger_object.log(self.file_object, 'Accuracy for RF:' + str(self.random_forest_score))
            #else:
            self.random_forest_score = roc_auc_score(y_test , self.prediction_random_forest)  # AUC for Random Forest
            self.logger_object.log(self.file_object, 'AUC for RF:' + str(self.random_forest_score))

            # comparing the two models
            if (self.random_forest_score < self.xgboost_score):
                return 'XGBoost', self.xgboost
            else:
                return 'RandomForest', self.random_forest

        except Exception as e:
            self.logger_object.log(self.file_object , 'Exception occured in get_best_model method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,  'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
            raise Exception()
















