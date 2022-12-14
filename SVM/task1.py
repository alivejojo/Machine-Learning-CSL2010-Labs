# -*- coding: utf-8 -*-
"""lab6_task1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PUJtLWihX7LZg6DU9E1g3qbHLIRlIdcq
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/gdrive')

from google.colab import drive
drive.mount('/content/drive')

df =  pd.read_csv("/content/drive/MyDrive/Dataset.csv")
df.head()

df.shape

"""Features - X1, x2 

Target - Target
"""

X = df.iloc[:,:2]
y = df.iloc[:,2]

from sklearn.model_selection import train_test_split

train_ , test_ = train_test_split(df, test_size = 0.2, random_state = 21)
X_train = train_.iloc[:,:-1]
y_train = train_.iloc[:,-1]
X_test = test_.iloc[:,:-1]
y_test = test_.iloc[:,-1]

from sklearn.svm import LinearSVC

classifier = LinearSVC(random_state = 21, C = 1)
classifier.fit(X_train,y_train)

classifier.score(X_test, y_test)

y_predicted_test = classifier.predict(X_test)
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test,y_predicted_test))
print(classification_report(y_test,y_predicted_test))
