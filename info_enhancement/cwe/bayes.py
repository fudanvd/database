import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV


def trainModel(X1, Y1):
    clf_Mu = MultinomialNB()
    param_grid = [{'alpha':np.arange(0.9,1.1,0.1),
              'fit_prior':['True','False']}]
    grid_search = GridSearchCV(clf_Mu, param_grid, cv = 3,
                          scoring = 'accuracy',
                          return_train_score = True)
    grid_search.fit(X1,Y1)

    return grid_search.best_estimator_

def bayesResult(final_model, X_test):
    X_test_prepared = final_model.predict(X_test)
    return X_test_prepared

if __name__ == '__main__':
    X = np.array([[1.14, 1.78],[1.18, 1.96],[1.20, 1.86],[1.26, 2.00],[1.28, 2.00],
             [1.30, 1.96],[1.24, 1.72],[1.36, 1.74],[1.38, 1.64],[1.38, 1.82],
             [1.38, 1.90],[1.40, 1.70],[1.48, 1.82],[1.54, 1.82],[1.56, 2.08]])
    Y = np.hstack((np.ones(6), np.ones(9)*2))
    trainModel(X, Y)