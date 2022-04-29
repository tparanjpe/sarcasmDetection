from cgi import test
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing
import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.svm import LinearSVC

#Random Forest Classifier
#K-Nearest Neighbors
#Linear Regression
#Adaboost


trainDF = pd.read_csv('training.csv')
testDF = pd.read_csv('testing.csv')

myVectorizer = TfidfVectorizer()
labelEncoder = preprocessing.LabelEncoder()

corpusTrain = trainDF['tweet_data'].tolist()
y_train = labelEncoder.fit_transform(trainDF['sarcasm_label'])
X_train = myVectorizer.fit_transform(corpusTrain)

smote = SMOTE()
X_train1, y_train1 = smote.fit_resample(X_train, y_train)

corpusTest = testDF['tweet_data'].tolist()
y_test = labelEncoder.fit_transform(testDF['sarcasm_label'])
X_test = myVectorizer.transform(corpusTest)




knn = KNeighborsClassifier(n_neighbors=2)
knn.fit(X_train1, y_train1)
y_pred = knn.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
print(f'KNN - accuracy: {accuracy}, f1: {f1}, recall: {recall}, precision: {precision}')

rfc = RandomForestClassifier(max_depth=2, random_state=0)
rfc.fit(X_train1, y_train1)
y_pred = rfc.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
print(f'RFC - accuracy: {accuracy}, f1: {f1}, recall: {recall}, precision: {precision}')

adaboost = AdaBoostClassifier(n_estimators=100, random_state=0)
adaboost.fit(X_train1, y_train1)
y_pred = adaboost.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
print(f'Adaboost - accuracy: {accuracy}, f1: {f1}, recall: {recall}, precision: {precision}')

svm = LinearSVC(class_weight='balanced')
svm.fit(X_train1, y_train1)
y_pred = svm.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
print(f'SVM - accuracy: {accuracy}, f1: {f1}, recall: {recall}, precision: {precision}')
