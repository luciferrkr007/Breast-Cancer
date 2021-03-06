# -*- coding: utf-8 -*-
"""breast cancer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YTXOdj6iDWg8bMPH54u8qTw_zBTgxy8_
"""

from google.colab import drive
drive.mount('/content/drive')

"""Importing Libraries"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import seaborn as sns; 
sns.set()
import matplotlib.pyplot as plt
# %matplotlib inline
from collections import Counter
from sklearn import tree
import graphviz 
import os
from sklearn import preprocessing 

from plotly.offline import init_notebook_mode, iplot, plot
import plotly as py
init_notebook_mode(connected=True)
import plotly.graph_objs as go
from wordcloud import WordCloud
from pandas_profiling import ProfileReport

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2, f_classif
from sklearn.model_selection import KFold
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import LinearSVC

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict

from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.decomposition import PCA

from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import CategoricalNB
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.model_selection import GridSearchCV

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier, XGBRFClassifier
from xgboost import plot_tree, plot_importance

from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score, roc_curve
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE

from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from scipy.stats import norm, skew, boxcox


import warnings
warnings.filterwarnings("ignore")

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

link='/content/drive/MyDrive/data.csv'
dataset=pd.read_csv(link)
dataset.head(5)

len(dataset.columns)

len(dataset)

"""About the dataset:
1. id: represents the ID of patient
2. Diagnosis : Diagnosis of cancerous cells(M=malignant, B=benign)
3. Radius_mean : mean radius of cells
4. texture_mean: Standard deviation of gray scale values
5. area_mean: mean of area of cells
6. smoothness mean: mean of local variation in radius lengths
7. compactness_mean: mean of perimeter^2/area -1
8. Concavity_mean: mean of severiity of concave portions to the contour
9. concave points_mean: mean for number of concave portions of the contour
10. symmetery_mean: mean of how symmetrical the cells are
11. fractal_dimension_mean = coastline approximation - 1
12. radius_se: standard error for the mean of distances from center to points on the perimeter
13. texture_se :  standard error for standard deviation of gray-scale values
14. perimeter_se: standard deviation of perimeter
15. area_se: standard deviation on area
16. smoothness_se: standard error for local variation in radius lengths
17. compactness_se: standard error for perimeter^2 / area - 1.0
18. concavity_se: standard error for severity of concave portions of the contour
19. concave points_se: standard error for number of concave portions of the contour
20. symmetery_se: standard deviation of symmetrical data iof cells
21. fractal_dimension_se: standard error for "coastline approximation" - 1
22. radius_worst: "worst" or largest mean value for mean of distances from center to points on the perimeter
23. texture_worst: "worst" or largest mean value for standard deviation of gray-scale values
24. perimeter_worst: "worst" or largest mean value for standard deviation of gray-scale values
25. area_worst: "worst" or largest mean value for standard deviation of gray-scale values
26. smoothness_worst --> "worst" or largest mean value for local variation in radius lengths
27. compactness_worst --> "worst" or largest mean value for perimeter^2 / area - 1.0
28. concavity_worst --> "worst" or largest mean value for severity of concave portions of the contour
29. concave points_worst --> "worst" or largest mean value for number of concave portions of the contour
30. symmetery_worst:  "worst" or largest mean value for standard deviation of gray-scale values
31. fractal_dimension_worst--> "worst" or largest mean value for "coastline approximation" - 1

"""

dataset.drop('id', inplace=True, axis=1)
dataset.drop('Unnamed: 32', inplace=True, axis=1)

dataset.info()

"""No null values"""

dataset.describe()

def detect_outliers(df,features):
    outlier_indices = []
    
    for c in features:
        Q1 = np.percentile(df[c],25)
        Q3 = np.percentile(df[c],75)
        IQR = Q3 - Q1
        outlier_step = IQR * 1.5
        outlier_list_col = df[(df[c] < Q1 - outlier_step) | (df[c] > Q3 + outlier_step)].index
        outlier_indices.extend(outlier_list_col)
    
    outlier_indices = Counter(outlier_indices)
    multiple_outliers = list(i for i, v in outlier_indices.items() if v > 2)
    
    return multiple_outliers

columns=list(dataset.columns)
columns.remove('diagnosis')

dataset.loc[detect_outliers(dataset,columns)]

dataset = dataset.drop(detect_outliers(dataset,columns),axis = 0).reset_index(drop = True)

for i in columns:
    dataset = dataset[dataset[i] != 0]

dataset

dataset.describe()

"""Correlation"""

plt.figure(figsize=(12,8))
sns.heatmap(dataset.corr(), cmap='Set1', linewidths=2)
plt.show()

dataset.agg(['skew'])

skews = ['area_mean', 'concavity_mean', 'radius_se', 'perimeter_se', 'area_se', 'smoothness_se', 
         'compactness_se', 'symmetry_se', 'fractal_dimension_se', 'area_worst', 'compactness_worst', 
         'fractal_dimension_worst' ]

for i in skews:
    sns.set_style('darkgrid')
    sns.distplot(dataset[i], fit = norm)
    plt.title('Skeweed')
    plt.show()
    (mu, sigma) = norm.fit(dataset[i])
    print("mu {} : {}, sigma {} : {}".format(i, mu, i, sigma))
    print()
    
    dataset[i], lam = boxcox(dataset[i])

    sns.set_style('darkgrid')
    sns.distplot(dataset[i], fit = norm)
    plt.title('Transformed')
    plt.show()
    (mu, sigma) = norm.fit(dataset[i])
    print("mu {} : {}, sigma {} : {}".format(i, mu, i, sigma))
    print()

dataset.agg(['skew', 'kurtosis']).transpose()

dataset['diagnosis'].unique()

unique_mapping={'M':0, 'B':1}
dataset['diagnosis']=dataset['diagnosis'].map(unique_mapping)

X=dataset[columns]
Y=dataset['diagnosis']

X_train, X_test, y_train, y_test= train_test_split(X,Y,test_size=1/3, random_state=42)

X_valid, X_test, y_valid, y_test= train_test_split(X_test, y_test, test_size=0.5, random_state=42)

print(f'Total # of sample in whole dataset: {len(X)}')
print(f'Total # of sample in train dataset: {len(X_train)}')
print(f'Total # of sample in validation dataset: {len(X_valid)}')
print(f'Total # of sample in test dataset: {len(X_test)}')

"""Pipeline"""

pipeline_GaussianNB = Pipeline([("scaler",StandardScaler()),
                     ("pipeline_GaussianNB",GaussianNB())])

pipeline_BernoulliNB = Pipeline([("scaler",StandardScaler()),
                     ("pipeline_BernoulliNB",BernoulliNB())])

pipeline_LogisticRegression = Pipeline([("scaler",StandardScaler()),
                     ("pipeline_LogisticRegression",LogisticRegression())])

pipeline_RandomForest = Pipeline([("scaler",StandardScaler()),
                     ("pipeline_RandomForest",RandomForestClassifier())])

pipeline_SVM = Pipeline([("scaler",StandardScaler()),
                     ("pipeline_SVM",SVC())])

pipeline_DecisionTree = Pipeline([("scaler",StandardScaler()),
                     ("pipeline_DecisionTree",DecisionTreeClassifier())])

pipeline_KNN = Pipeline([("scaler",StandardScaler()),
                     ("pipeline_KNN",KNeighborsClassifier())])

pipeline_GBC = Pipeline([("scaler",StandardScaler()), (
                        "pipeline_GBC",GradientBoostingClassifier())])

pipeline_SGD = Pipeline([("scaler",StandardScaler()), 
                        ("pipeline_SGD",SGDClassifier(max_iter=5000, random_state=0))])

pipeline_NN = Pipeline([("scaler",StandardScaler()), 
                        ("pipeline_NN",MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5000, 10), random_state=1))])

pipelines = [pipeline_GaussianNB, pipeline_BernoulliNB, pipeline_LogisticRegression,
             pipeline_RandomForest, pipeline_SVM, pipeline_DecisionTree, pipeline_KNN,
             pipeline_GBC, pipeline_SGD, pipeline_NN]

pipe_dict = {0: "GaussianNB", 1: "BernoulliNB", 2: "LogisticRegression",3: "RandomForestClassifier", 4: "SupportVectorMachine", 5: "DecisionTreeClassifier",
            6: "KNeighborsClassifier", 7: "GradientBoostingClassifier", 8:"Stochastic Gradient Descent", 9: "Neural Nets"}

for pipe in pipelines:
    pipe.fit(X_train, y_train)

cv_results_acc = []

for i, model in enumerate(pipelines):
    cv_score = cross_val_score(model, X_train, y_train, scoring = "accuracy", cv = 10)
    cv_results_acc.append(cv_score)
    print("%s: %f" % (pipe_dict[i], cv_score.mean()*100))

"""SVM and LR having maximu cross validation accuracy and Neaural Nets is second highest.

## Metrics theory

1. Accuracy: In multilabel classification, this function computes subset accuracy: the set of labels predicted for a sample must exactly match the corresponding set of labels in y_true.

2. Balanced Accuracy: The balanced accuracy in binary and multiclass classification problems to deal with imbalanced datasets. It is defined as the average of recall obtained on each class.

3. Cohen's Kappa: The function cohen_kappa_score computes Cohen???s kappa statistic. This measure is intended to compare labelings by different human annotators, not a classifier versus a ground truth.The kappa score (see docstring) is a number between -1 and 1. Scores above .8 are generally considered good agreement; zero or lower means no agreement (practically random labels).

4. Average Precision: AP summarizes a precision-recall curve as the weighted mean of precisions achieved at each threshold, with the increase in recall from the previous threshold used as the weight:

5. Log Loss:aka logistic loss or cross-entropy loss.This is the loss function used in (multinomial) logistic regression and extensions of it such as neural networks, defined as the negative log-likelihood of a logistic model that returns y_pred probabilities for its training data y_true. The log loss is only defined for two or more labels. For a single sample with true label  
y
???
{
0
,
1
}
  and a probability estimate  
p
=
Pr
(
y
=
1
)
 
6. Jaccard Coefficient Score: The Jaccard index, or Jaccard similarity coefficient, defined as the size of the intersection divided by the size of the union of two label sets, is used to compare set of predicted labels for a sample to the corresponding set of labels in y_true.

## SVM
"""

train_score = pipeline_SVM.score(X_train, y_train)
print(f'Train score of trained model     : {train_score*100}')

validation_score = pipeline_SVM.score(X_valid, y_valid)
print(f'Validation score of trained model: {validation_score*100}')

test_score = pipeline_SVM.score(X_test, y_test)
print(f'Test score of trained model      : {test_score*100}')

pred_svm = pipeline_SVM.predict(X_test)

conf_matrix = confusion_matrix(pred_svm, y_test)

print(f'Confussion Matrix: \n{conf_matrix}\n')

sns.heatmap(conf_matrix, annot=True)
plt.show()

tn = conf_matrix[0,0]
fp = conf_matrix[0,1]
tp = conf_matrix[1,1]
fn = conf_matrix[1,0]

total = tn + fp + tp + fn
real_positive = tp + fn
real_negative = tn + fp

accuracy  = (tp + tn) / total 
precision = tp / (tp + fp) 
recall    = tp / (tp + fn) 
f1score  = 2 * precision * recall / (precision + recall)
specificity = tn / (tn + fp) 
error_rate = (fp + fn) / total 
prevalence = real_positive / total
miss_rate = fn / real_positive 
fall_out = fp / real_negative 

print(f'Accuracy    : {accuracy}')
print(f'Precision   : {precision}')
print(f'Recall      : {recall}')
print(f'F1 score    : {f1score}')
print(f'Specificity : {specificity}')
print(f'Error Rate  : {error_rate}')
print(f'Prevalence  : {prevalence}')
print(f'Miss Rate   : {miss_rate}')
print(f'Fall Out    : {fall_out}')

print(classification_report(pred_svm, y_test))

print("accuracy           :", metrics.accuracy_score(y_test, pred_svm)*100)
print("balanced_accuracy  :", metrics.balanced_accuracy_score(y_test, pred_svm))
print("Cohen???s Kappa      :", metrics.cohen_kappa_score(y_test, pred_svm))
print("average_precision  :", metrics.average_precision_score(y_test, pred_svm)*100)
print("neg_log_loss       :", metrics.log_loss(y_test, pred_svm)*100)
print("jaccard            :", metrics.jaccard_score(y_test, pred_svm)*100)

"""## LR"""

train_score = pipeline_LogisticRegression.score(X_train, y_train)
print(f'Train score of trained model     : {train_score*100}')

validation_score = pipeline_LogisticRegression.score(X_valid, y_valid)
print(f'Validation score of trained model: {validation_score*100}')

test_score = pipeline_LogisticRegression.score(X_test, y_test)
print(f'Test score of trained model      : {test_score*100}')

pred_lr = pipeline_LogisticRegression.predict(X_test)

conf_matrix = confusion_matrix(pred_lr, y_test)

print(f'Confussion Matrix: \n{conf_matrix}\n')

sns.heatmap(conf_matrix, annot=True)
plt.show()

tn = conf_matrix[0,0]
fp = conf_matrix[0,1]
tp = conf_matrix[1,1]
fn = conf_matrix[1,0]

total = tn + fp + tp + fn
real_positive = tp + fn
real_negative = tn + fp

accuracy  = (tp + tn) / total 
precision = tp / (tp + fp) 
recall    = tp / (tp + fn) 
f1score  = 2 * precision * recall / (precision + recall)
specificity = tn / (tn + fp) 
error_rate = (fp + fn) / total 
prevalence = real_positive / total
miss_rate = fn / real_positive 
fall_out = fp / real_negative 

print(f'Accuracy    : {accuracy}')
print(f'Precision   : {precision}')
print(f'Recall      : {recall}')
print(f'F1 score    : {f1score}')
print(f'Specificity : {specificity}')
print(f'Error Rate  : {error_rate}')
print(f'Prevalence  : {prevalence}')
print(f'Miss Rate   : {miss_rate}')
print(f'Fall Out    : {fall_out}')

print(classification_report(pred_lr, y_test))

print("accuracy           :", metrics.accuracy_score(y_test, pred_lr)*100)
print("balanced_accuracy  :", metrics.balanced_accuracy_score(y_test, pred_lr))
print("Cohen???s Kappa      :", metrics.cohen_kappa_score(y_test, pred_lr))
print("average_precision  :", metrics.average_precision_score(y_test, pred_lr)*100)
print("neg_log_loss       :", metrics.log_loss(y_test, pred_lr)*100)
print("jaccard            :", metrics.jaccard_score(y_test, pred_lr)*100)

"""## Neural Nets"""

train_score = pipeline_NN.score(X_train, y_train)
print(f'Train score of trained model     : {train_score*100}')

validation_score = pipeline_NN.score(X_valid, y_valid)
print(f'Validation score of trained model: {validation_score*100}')

test_score = pipeline_NN.score(X_test, y_test)
print(f'Test score of trained model      : {test_score*100}')

pred_nn = pipeline_NN.predict(X_test)

conf_matrix = confusion_matrix(pred_nn, y_test)

print(f'Confussion Matrix: \n{conf_matrix}\n')

sns.heatmap(conf_matrix, annot=True)
plt.show()

tn = conf_matrix[0,0]
fp = conf_matrix[0,1]
tp = conf_matrix[1,1]
fn = conf_matrix[1,0]

total = tn + fp + tp + fn
real_positive = tp + fn
real_negative = tn + fp

accuracy  = (tp + tn) / total 
precision = tp / (tp + fp) 
recall    = tp / (tp + fn) 
f1score  = 2 * precision * recall / (precision + recall)
specificity = tn / (tn + fp) 
error_rate = (fp + fn) / total 
prevalence = real_positive / total
miss_rate = fn / real_positive 
fall_out = fp / real_negative 

print(f'Accuracy    : {accuracy}')
print(f'Precision   : {precision}')
print(f'Recall      : {recall}')
print(f'F1 score    : {f1score}')
print(f'Specificity : {specificity}')
print(f'Error Rate  : {error_rate}')
print(f'Prevalence  : {prevalence}')
print(f'Miss Rate   : {miss_rate}')
print(f'Fall Out    : {fall_out}')

print(classification_report(pred_nn, y_test))

print("accuracy           :", metrics.accuracy_score(y_test, pred_nn)*100)
print("balanced_accuracy  :", metrics.balanced_accuracy_score(y_test, pred_nn))
print("Cohen???s Kappa      :", metrics.cohen_kappa_score(y_test, pred_nn))
print("average_precision  :", metrics.average_precision_score(y_test, pred_nn)*100)
print("neg_log_loss       :", metrics.log_loss(y_test, pred_nn)*100)
print("jaccard            :", metrics.jaccard_score(y_test, pred_nn)*100)

"""## Metrics table"""

metrics_data = [
['Accuracy',metrics.accuracy_score(y_test, pred_svm)*100 ,metrics.accuracy_score(y_test, pred_lr)*100 ,metrics.accuracy_score(y_test, pred_nn)*100],
['Balanced Accuracy',metrics.balanced_accuracy_score(y_test, pred_svm),metrics.balanced_accuracy_score(y_test, pred_lr),metrics.balanced_accuracy_score(y_test, pred_nn)],
['Cohens Kappa',metrics.cohen_kappa_score(y_test, pred_svm),metrics.cohen_kappa_score(y_test, pred_lr),metrics.cohen_kappa_score(y_test, pred_nn)],
['Average Precision',metrics.average_precision_score(y_test, pred_svm)*100,metrics.average_precision_score(y_test, pred_lr)*100,metrics.average_precision_score(y_test, pred_nn)*100 ],
['Log Loss', metrics.log_loss(y_test, pred_svm)*100,metrics.log_loss(y_test, pred_lr)*100,metrics.log_loss(y_test, pred_nn)*100],
['Jaccard',  metrics.jaccard_score(y_test, pred_svm)*100, metrics.jaccard_score(y_test, pred_lr)*100, metrics.jaccard_score(y_test, pred_nn)*100]     
          ]

df=pd.DataFrame(metrics_data, columns=['Metric','SVM', 'LR', 'NN'])

df

"""Logistic Regression is a better model for the wiscosin cancer dataset."""

