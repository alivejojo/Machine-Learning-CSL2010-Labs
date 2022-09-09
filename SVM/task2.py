# -*- coding: utf-8 -*-
"""lab6_task2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k6bZbP8nbRpUrrYu2eoxm4qY1WlA9j3u
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/gdrive')

df = pd.read_csv('/content/gdrive/MyDrive/iml/Dataset_2.csv')
df.head()

df.shape

# removing any null values
print(df.loc[:, df.isnull().any()].columns)

df.iloc[540]

# removing outliers
# all entries should be positive 
for i in range(len(list(df.columns))):
  for j in range(len(df)):
    if df.iloc[j,i]<0:
      df.iloc[j,i] = df[list(df.columns)[i]].mean()

df.iloc[540]

"""Randomly select any 3 features out of 6 to plot 3D plot. """

df.describe()

# putting features and target into different variables
df_features = df.drop(['CreditCard'] , axis =1)
df_target = df['CreditCard']

df_features.head()

df_target.head()

# choosing the best 3 features to be used in the model 
# find correlation of all features with the target
import seaborn as sns
corrmat = df.corr()
top_corr_features = corrmat.index
g = sns.heatmap(df[top_corr_features].corr(), annot=True, cmap = 'RdYlGn' )

# the highest correlation of target_variable is with [Age, Experience, Income]

# 3D plotting
from mpl_toolkits import mplot3d
ax = plt.axes(projection="3d")
fig = plt.figure(figsize = (20, 19))
ax.set_xlabel('Age')
ax.set_ylabel('Experience')
ax.set_zlabel('Mortgage')


ax.scatter3D(df_features['Age'],df_features['Experience'], df_features['Mortgage'])
plt.show()

# now retaining only the best three columns 
df_features_best = df_features.drop(columns = ['CCAvg','Income','Securities'])
df_features_best.head()

# splitting the features and target dataFrames in 80:20 ratio 
from sklearn.model_selection import train_test_split

X_train , X_test, y_train, y_test = train_test_split(df_features_best, df_target, random_state = 0)

from sklearn.svm import LinearSVC

# before training we must standardize the features 
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.fit_transform(X_test)

for c in [0.0001, 0.001, 0.01, 0.1, 1, 10,100,1000]:
  print('C = ',c)
  svclassifier = LinearSVC(C=c , random_state=0, max_iter = 3000)
  svclassifier.fit(X_train_scaled, y_train)
  print("Score on test data = ", svclassifier.score(X_test_scaled, y_test))
  y_pred = svclassifier.predict(X_test_scaled)
  print(confusion_matrix(y_test,y_pred))
  print()
  print(classification_report(y_test,y_pred))

import warnings
warnings.filterwarnings('ignore')

# using GridSearchCV for parameter tuning
from sklearn.model_selection import GridSearchCV

param_grid={'C':[ 0.001, 0.0001, 0.01, 0.1, 1, 10 ,100 ,1000]}
grid = GridSearchCV(LinearSVC(random_state = 0), param_grid, cv=5)
grid.fit(X_train_scaled, y_train)
#finding the best value of C
print(grid.best_params_)

# given that SVM is failing to converge for many values of C(despite increasing max_iter = 100000), 
# we question whether the data is actually linearly seperable or not
