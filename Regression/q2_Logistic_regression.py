# -*- coding: utf-8 -*-
"""q2_logistic.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17U4Yj22gdMMjS7mTtSftI2XDDlvr8i1t
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from google.colab import files
uploaded = files.upload()

df = pd.read_csv("logistic_regression_dataset.csv")
df.head()

# need to apply onehotencoder to Gender column as it is categorical but not ordered. 
from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder(handle_unknown='ignore')

enc_df = pd.DataFrame(enc.fit_transform(df[['Gender']]).toarray())
df = df.drop(columns = ['Gender'])
df = df.join(enc_df)

df = df.drop(columns = 1)
df.rename(columns={0: "Female"})

from sklearn.model_selection import train_test_split
train, test = train_test_split(df, test_size =0.2)

train.head()

X_train = train[['Age', 'EstimatedSalary', 0]]
y_train = train[['Purchased']]
X_test = test[['Age', 'EstimatedSalary', 0]]
y_test = test[['Purchased']]

print( "amount of purchased ",len(X_train==1) )
print( "amount of NOT purchased ",len(X_train==0))

X_train.head()

# now we scale age, estimatedsalary and female or not. 
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range = (0,1))

X_train_scaled = X_train.copy()
X_test_scaled = X_train.copy()

X_train_scaled = scaler.fit_transform(X_train[['Age', 'EstimatedSalary',0]])
X_test_scaled = scaler.fit_transform(X_test[['Age', 'EstimatedSalary',0]])

from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
logreg.fit(X_train_scaled,y_train)
y_pred = logreg.predict(X_test_scaled)
print(y_pred)

from sklearn import metrics
cnf_matrix = metrics.confusion_matrix(y_test.to_numpy(), y_pred)
cnf_matrix

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
class_names=[0,1] # name  of classes
fig, ax = plt.subplots()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)
# create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
