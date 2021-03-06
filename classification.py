#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 11:32:25 2021

@author: incognito
"""

from sklearn.datasets import fetch_openml
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_val_predict
from sklearn.base import clone, BaseEstimator
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, precision_recall_curve, roc_curve, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

mnist = fetch_openml('mnist_784', version=1, as_frame=False)

X, y = mnist["data"], mnist["target"]
some_digit = X[0]
some_digit_image = some_digit.reshape(28,28)

plt.imshow(some_digit_image, cmap= matplotlib.cm.binary, interpolation="nearest")
plt.axis("off")
plt.show()

'''SPLITTING TRAINING AND TESTING SETS'''

X_train, X_test, y_train, y_test = X[:60000], X[60000:], y[:60000], y[60000:]

'''shuffling the training set; this will guarantee that all cross-validation folds will
be similar
'''
shuffle_index = np.random.permutation(60000)
X_train, y_train = X_train[shuffle_index], y_train[shuffle_index]

'''Distinguishing between two classes. 5 or not 5'''
y_train_5 = (y_train == 5)
y_test_5 = (y_test == 5)

'''Stochastic Gradient Classifier'''
sgd_clf = SGDClassifier(max_iter=1000, tol=1e-3, random_state=42)
sgd_clf.fit(X_train, y_train_5)

sgd_clf.predict([some_digit])

'''IMPLEMENTING CROSS-VALIDATION'''
'''performing stratified sampling to produce folds that contain a representative ratio of each class.
'''
skfolds = StratifiedKFold(n_splits=3, random_state=42)

'''At each iteration the code creates a clone of the classifier, trains that clone on the training folds,
and makes predictions on the test fold.
'''
for train_index, test_index in skfolds.split(X_train, y_train_5):
    clone_clf = clone(sgd_clf)
    x_train_folds = X_train[train_index]
    y_train_folds = (y_train_5[train_index])
    x_test_fold = X_train[test_index]
    y_test_fold =(y_train_5[test_index])
    
    clone_clf.fit(x_train_folds, y_train_folds)
    y_pred = clone_clf.predict(x_test_fold)
    
    '''it counts the number of correct predictions and outputs the ratio of correct predictions.
    '''
    n_correct = sum(y_pred == y_test_fold)
    print(n_correct/ len(y_pred))

'''using the cross_val_score() method'''
cross_val_score(sgd_clf, X_train, y_train_5, cv=3, scoring="accuracy")

'''A never 5 classifier ccurracy prediction'''
class Never5Classifier(BaseEstimator):
    def fit(self, X, y=None):
        pass
    def predict(self,X):
        return np.zeros((len(X),1), dtype=bool)
    
never_5_clf = Never5Classifier()
cross_val_score(never_5_clf, X_train, y_train_5, cv=3, scoring="accuracy")    

'''Confusion Matrix'''
y_train_pred = cross_val_predict(sgd_clf, x_train, y_train_5, cv=3)
confusion_matrix(y_train_5, y_train_pred)
confusion_matrix(y_train_5, y_train_perfect_predictions)

'''Precision and Recall'''
'''Precision'''
precision_score(y_train_5, y_pred)

'''Recall'''
recall_score(y_train_5, y_train_pred)

'''F1'''
f1_score(y_train_5, y_pred)

'''DECISION THRESHOLD'''
'''returning a score for each instance
'''
y_scores = sgd_clf.decision_function([some_digit])
print(y_scores)
'''setting a threshold manually'''
threshold = 200000
y_some_digit_pred = (y_scores > threshold)
y_scores = cross_val_predict(sgd_clf, X_train, y_train_5, cv=3, method="decision_function")
precisions, recalls, thresholds = precision_recall_curve(y_train_5, y_scores)

'''Plotting precision_recall vs threshold curve'''
def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
    plt.plot(thresholds, precisions[:-1], "b--", label="Precisions")
    plt.plot(thresholds, recalls[:-1],"g-", label="Recall")
    plt.xlabel("Threshold")
    plt.legend(loc="upper left")
    plt.ylim([0,1])

plot_precision_recall_vs_threshold(precisions, recalls, thresholds)
plt.show()

'''Precision ve Recall plot'''
def plot_precision_vs_recall(precisions, recalls):
    plt.plot(recalls[:-1], precisions[:-1], "b")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    #plt.ylim([0,1])

plot_precision_vs_recall(precisions, recalls)
plt.show()

'''Getting the highest precision score'''
90_percent_threshold = thresholds[np.argmax(precisions >= 0.90)]
y_train_pred_90 = (y_scores >= 90_percent_threshold)

#the precisiion score
precision_score(y_train_5, y_train_pred_90)
recall_score(y_train_5, y_train_pred_90)

'''PLotting the ROC curvee'''
fpr, tpr, thresholds = roc_curve(y_train_5, y_scores)
def plot_roc_curve(fpr, tpr, label=None):
    plt.plot(fpr, tpr, linewidth=2, label=label)
    plt.plot([0,1],[0,1], 'k--')
    plt.axis([0,1,0,1])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    
plot_roc_curve(fpr, tpr)    
plt.show()

'''gettting the area under the curve score'''
roc_auc_score(y_train_5, y_scores)

'''training a Random FOrest'''
forest_clf = RandomForestClassifier(random_state=42)
y_probas_forest = cross_val_predict(forest_clf,  X_train, y_train_5, cv=3, method="predict_proba")
y_scores_forest = y_probas_forest[:,1]
fpr_forest, tpr_forest, thresholds_forest = roc_curve(y_train_5, y_scores_forest)

'''comparing respective ROC curves'''
plt.plot(fpr, tpr, "b:",label="SGD")
plot_roc_curve(fpr_forest, tpr_forest, "Random Forest")
plt.legend(loc="bottom right")
plt.show()


'''Random Forest prediction'''
y_train_pred_forest = cross_val_predict(forest_clf, X_train, y_train_5, cv=3)

precision_score(y_train_5, y_train_pred_forest)
recall_score(y_train_5, y_train_pred_forest)

'''MULTICLASSIFICATION'''
sgd_clf.fit(X_train, y_train)
sgd_clf.predict([some_digit])

'''scores'''
some_digit_scores = sgd_clf.decision_function([some_digit])

'''max score'''
np.argmax(some_digit_scores)

'''target classes'''
sgd_clf.classes_

'''forcing scikit-learn to use OvO'''
ovo_clf = OneVsOneClassifier(SGDClassifier(random_state=42))
ovo_clf.fit(X_train, y_train)
ovo_clf.predict([some_digit])

'''random forest classifier'''
forest_clf.fit(X_train, y_train)
forest_clf.predict([some_digit])

#getting the probabilities of the targets
forest_clf.predict_proba([some_digit])

'''measuring the performance'''
cross_val_score(sgd_clf, X_train, y_train, cv=3, scoring="accuracy")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train.astype(np.float64))
cross_val_score(sgd_clf, X_train_scaled, y_train, cv=3, scoring="accuracy")

'''ERROR ANALYSIS'''
y_train_pred = cross_val_predict(sgd_clf, X_train_scaled, y_train, cv=3)
conf_mx = confusion_matrix(y_train, y_train_pred)

'''plotting'''
plt.matshow(conf_mx, cmap=plt.cm.gray)
plt.show()

'''computinmg the error rates'''
row_sums = conf_mx.sum(axis=1, keepdims=True)
norm_conf_mx = conf_mx / row_sums

'''filling the diagonals with zeros to keep only the  errors'''
np.fill_diagonal(norm_conf_mx, 0)
plt.matshow(norm_conf_mx, cmap=plt.cm.gray)
plt.show()

'''analysing the 3/5 errror'''
cl_a, cl_b = 3,5
X_aa = X_train[(y_train == cl_a) & (y_train_pred == cl_a)]
X_ab = X_train[(y_train == cl_a) & (y_train_pred == cl_b)] 
X_ba = X_train[(y_train == cl_b) & (y_train_pred == cl_a)]
X_bb = X_train[(y_train == cl_b) & (y_train_pred == cl_b)]
plt.figure(figsize=(8,8))
plt.subplot(221); plot_digits(X_aa[:25], images_per_row=5)
plt.subplot(222); plot_digits(X_ab[:25], images_per_row=5)
plt.subplot(223); plot_digits(X_bb[:25], images_per_row=5)
plt.subplot(224); plot_digits(X_bb[:25], images_per_row=5)

'''MULTILABEL CLASSIFICATION'''
y_train_large = (y_train >= 7)
y_train_odd = (y_train % 2 == 1)
y_multilabel = np.c_[y_train_large, y_train_odd]

knn_clf = KNeighborsClassifier()
knn_clf.fit(X_train, y_multilabel)

knn_clf.predict([some_digit])

'''Measuring the perfomance'''
y_train_knn_pred = cross_val_predict(knn_clf, X_train, y_train, cv=3)
f1_score(y_train, y_train_knn_pred, average="macro")

'''MULTIOUTPUT CLASSIFICATION'''
'''adding noise to their pixel intensities'''
noise = rnd.randint(0,100,(len(X_train),784))
noise = rnd.randint(0,100,(len(X_test),784))
X_train_mod = X_train + noise
X_test_mod = X_test + noise
y_train_mod = X_train
y_test_mod = x_test
knn_clf.fit(X_train_mod, y_train_mod)
clean_digit = knn_clf.predict([X_test_mod[some_index]])
plot_digit(clean_digit)
