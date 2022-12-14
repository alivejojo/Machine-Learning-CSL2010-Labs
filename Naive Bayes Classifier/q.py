# -*- coding: utf-8 -*-
"""B20BB047_lab14.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YACFmhIHseOHeSU7_umo_47NrMA8q77L
"""

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

from google.colab import files
uploaded = files.upload()

df = pd.read_csv('diabetes 2.csv')
df.head()

df.shape

"""# Pre-processing

## Null value handling
"""

def check_zeros(clm):

  s=0
  for i in range(len(clm)):
    if clm[i] == [0]: 
      s = s + 1
  return s

print("number of zeros in : ")
for i in list(df.columns):
  
  print(i, " -> ", check_zeros(   df[[i]].to_numpy()  ))

# zeros in Pregnancies and Outcomes makes sense. 
# 0's in Glucose, BloodPressure, SkinThickness, BMI don't make sense
# we impute them by mean values of the respective features

def impute_by_mean (clm):

  for i in range(df[clm].values.shape[0]):
    if df[clm].values[i] == 0:
      df[clm].values[i] = df[clm].mean()

impute_by_mean('Glucose')
impute_by_mean('BloodPressure')
impute_by_mean('SkinThickness')
impute_by_mean('BMI')

print("number of zeros in : ")
for i in list(df.columns):
  
  print(i, " -> ", check_zeros(   df[[i]].to_numpy()  ))

"""## Splitting"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(df.drop(columns=['Outcome']), df['Outcome'], test_size = 0.3)

X_train_scaled_df = pd.DataFrame(X_train_scaled, columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin','BMI', 'DiabetesPedigreeFunction', 'Age'])
X_train_scaled_df

y_train_df = pd.DataFrame(y_train, columns=['Outcome'])
X_test_scaled_df = pd.DataFrame(X_test_scaled,  columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin','BMI', 'DiabetesPedigreeFunction', 'Age'])

"""## Scaling"""

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""## EDA"""

# plotting various features.
plt.title("Pregnancies") 
plt.hist(X_train_scaled_df['Pregnancies'])
plt.show()
plt.title("Glucose") 
plt.hist(X_train_scaled_df['Glucose'])
plt.show()
plt.title("BloodPressure") 
plt.hist(X_train_scaled_df['BloodPressure'])
plt.show()
plt.title("SkinThickness") 
plt.hist(X_train_scaled_df['SkinThickness'])
plt.show()
plt.title("Insulin") 
plt.hist(X_train_scaled_df['Insulin'])
plt.show()
plt.title("BMI") 
plt.hist(X_train_scaled_df['BMI'])
plt.show()
plt.title("DiabetesPedigreeFunction") 
plt.hist(X_train_scaled_df['DiabetesPedigreeFunction'])
plt.show()
plt.title("Age") 
plt.hist(X_train_scaled_df['Age'])
plt.show()
# naive baye's requires independence in features. Let's plot the covariance matrix to see how true this is.

"""As we can see, not all features have a gaussian distribution. 

Glucose, blood pressure, BMI (skewed) and Skin thickness have somewhat of a gaussian distribution. 

The extreme range = [-5,8]
Hence we can create bins of 0.5

# Model Building

## Library
"""

from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()
ypred_lib = gnb.fit(X_train_scaled, y_train).predict(X_test_scaled)
from sklearn.metrics import accuracy_score

print(accuracy_score(ypred_lib,y_test))

"""## Scratch"""

# prior = [ P(outcome=0) , P(outcome=1)]
c=0
for i in range(len(y_train.to_numpy())):
    if y_train.to_numpy()[i]==0:
        c+=1

prior = np.array([c/768,(768-c)/768])
prior

# discretize all variables
plt.hist(X_train_scaled_df['Pregnancies'], bins = 20)

X_train_scaled_df_copy2 = X_train_scaled_df.copy()
# X_train_scaled_df_copy = pd.cut(X_train_scaled_df, bins = 20)
X_train_scaled_df_copy2['Pregnancies'] = pd.cut(X_train_scaled_df.Pregnancies, bins = 20)
X_train_scaled_df_copy2['Glucose'] = pd.cut(X_train_scaled_df.Glucose, bins = 20)
X_train_scaled_df_copy2['BloodPressure'] = pd.cut(X_train_scaled_df.BloodPressure, bins = 20)
X_train_scaled_df_copy2['Insulin'] = pd.cut(X_train_scaled_df.Insulin, bins = 20)
X_train_scaled_df_copy2['BMI'] = pd.cut(X_train_scaled_df.BMI, bins = 20)
X_train_scaled_df_copy2['SkinThickness'] = pd.cut(X_train_scaled_df.SkinThickness, bins = 20)
X_train_scaled_df_copy2['DiabetesPedigreeFunction'] = pd.cut(X_train_scaled_df.DiabetesPedigreeFunction, bins = 20)
X_train_scaled_df_copy2['Age'] = pd.cut(X_train_scaled_df.Age, bins = 20)

X_train_scaled_df_copy2

# implement naive bayes from scratch using EACH FEATURE INDEPENDENTLY with app bin size, and find classification accuracies

# using # of pregnancies
# creating bins of size 0.5 from [-5,8] 
counts_of_outcomes_Pregnancies = [[0,0] for i in range(25)]
freq_by_bins_Pregnancies = [0 for i in range(25)]

for i in range(len(X_train_scaled)):

    if X_train_scaled[i][0] < -5 or X_train_scaled[i][0] > 8:
        continue

    elif X_train_scaled[i][0] >= -5 and X_train_scaled[i][0] <-4.5:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[0][1]+=1
        else:
            counts_of_outcomes_Pregnancies[0][0]+=1
        freq_by_bins_Pregnancies[0] += 1 
    
    elif X_train_scaled[i][0] >= -4.5 and X_train_scaled[i][0] <-4:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[1][1]+=1
        else:
            counts_of_outcomes_Pregnancies[1][0]+=1
        freq_by_bins_Pregnancies[1] += 1 
    
    elif X_train_scaled[i][0] >= -4 and X_train_scaled[i][0] <-3.5:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[2][1]+=1
        else:
            counts_of_outcomes_Pregnancies[2][0]+=1
        freq_by_bins_Pregnancies[2] += 1

    elif X_train_scaled[i][0] >= -3.5 and X_train_scaled[i][0] <-3:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[3][1]+=1
        else:
            counts_of_outcomes_Pregnancies[3][0]+=1
        freq_by_bins_Pregnancies[3] += 1 

    elif X_train_scaled[i][0] >= -3 and X_train_scaled[i][0] <-2.5:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[4][1]+=1
        else:
            counts_of_outcomes_Pregnancies[4][0]+=1
        freq_by_bins_Pregnancies[4] += 1 

    elif X_train_scaled[i][0] >= -2.5 and X_train_scaled[i][0] <-2:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[5][1]+=1
        else:
            counts_of_outcomes_Pregnancies[5][0]+=1
        freq_by_bins_Pregnancies[5] += 1 


    elif X_train_scaled[i][0] >=-2 and X_train_scaled[i][0] <-1.5:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[6][1]+=1
        else:
            counts_of_outcomes_Pregnancies[6][0]+=1
        freq_by_bins_Pregnancies[6] += 1 

    elif X_train_scaled[i][0] >= -1.5 and X_train_scaled[i][0] <-1:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[7][1]+=1
        else:
            counts_of_outcomes_Pregnancies[7][0]+=1
        freq_by_bins_Pregnancies[7] += 1 

    elif X_train_scaled[i][0] >-1 and X_train_scaled[i][0] <-0.5:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[8][1]+=1
        else:
            counts_of_outcomes_Pregnancies[8][0]+=1
        freq_by_bins_Pregnancies[8] += 1 

    elif X_train_scaled[i][0] >= -0.5 and X_train_scaled[i][0] <0:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[9][1]+=1
        else:
            counts_of_outcomes_Pregnancies[9][0]+=1
        freq_by_bins_Pregnancies[9] += 1

    elif X_train_scaled[i][0] >= 0 and X_train_scaled[i][0] < 0.5:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[10][1]+=1
        else:
            counts_of_outcomes_Pregnancies[10][0]+=1
        freq_by_bins_Pregnancies[10] += 1

    elif X_train_scaled[i][0] >= 0.5 and X_train_scaled[i][0] <1:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[11][1]+=1
        else:
            counts_of_outcomes_Pregnancies[11][0]+=1
        freq_by_bins_Pregnancies[11] += 1

    elif X_train_scaled[i][0] >= 1 and X_train_scaled[i][0] < 1.5:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[12][1]+=1
        else:
            counts_of_outcomes_Pregnancies[12][0]+=1
        freq_by_bins_Pregnancies[12] += 1

    elif X_train_scaled[i][0] >= 1.5 and X_train_scaled[i][0] <2:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[13][1]+=1
        else:
            counts_of_outcomes_Pregnancies[13][0]+=1
        freq_by_bins_Pregnancies[13] += 1
    
    elif X_train_scaled[i][0] >= 2 and X_train_scaled[i][0] <2.5:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[14][1]+=1
        else:
            counts_of_outcomes_Pregnancies[14][0]+=1
        freq_by_bins_Pregnancies[14] += 1

    elif X_train_scaled[i][0] >= 2.5 and X_train_scaled[i][0] < 3:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[15][1]+=1
        else:
            counts_of_outcomes_Pregnancies[15][0]+=1
        freq_by_bins_Pregnancies[15] += 1

    elif X_train_scaled[i][0] >= 3.5 and X_train_scaled[i][0] <4:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[16][1]+=1
        else:
            counts_of_outcomes_Pregnancies[16][0]+=1
        freq_by_bins_Pregnancies[16] += 1

    elif X_train_scaled[i][0] >= 4 and X_train_scaled[i][0] < 4.5:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[17][1]+=1
        else:
            counts_of_outcomes_Pregnancies[17][0]+=1
        freq_by_bins_Pregnancies[17] += 1

    elif X_train_scaled[i][0] >= 4.5 and X_train_scaled[i][0] <5:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[18][1]+=1
        else:
            counts_of_outcomes_Pregnancies[18][0]+=1
        freq_by_bins_Pregnancies[18] += 1

    elif X_train_scaled[i][0] >= 5 and X_train_scaled[i][0] <5.5:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[19][1]+=1
        else:
            counts_of_outcomes_Pregnancies[19][0]+=1
        freq_by_bins_Pregnancies[19] += 1

    elif X_train_scaled[i][0] >= 5.5 and X_train_scaled[i][0] <6:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[20][1]+=1
        else:
            counts_of_outcomes_Pregnancies[20][0]+=1
        freq_by_bins_Pregnancies[20] += 1

    elif X_train_scaled[i][0] >= 6 and X_train_scaled[i][0] <6.5:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[21][1]+=1
        else:
            counts_of_outcomes_Pregnancies[21][0]+=1
        freq_by_bins_Pregnancies[21] += 1

    elif X_train_scaled[i][0] >= 6.5 and X_train_scaled[i][0] <7:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[22][1]+=1
        else:
            counts_of_outcomes_Pregnancies[22][0]+=1
        freq_by_bins_Pregnancies[22] += 1

    elif X_train_scaled[i][0] >= 7 and X_train_scaled[i][0] <7.5:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[23][1]+=1
        else:
            counts_of_outcomes_Pregnancies[23][0]+=1
        freq_by_bins_Pregnancies[23] += 1

    elif X_train_scaled[i][0] >= 7.5 and X_train_scaled[i][0] <8:
        if y_train[i] == 1:
            counts_of_outcomes_Pregnancies[24][1]+=1
        else:
            counts_of_outcomes_Pregnancies[24][0]+=1
        freq_by_bins_Pregnancies[24] += 1

# now for each test_sample we use pregnancy to see whether it gives a good prediction or not.
y_pred = []
for i in X_test_scaled[:,0]:

    if i >= -5 and i <-4.5:
        y_pred.append(counts_of_outcomes_Pregnancies[0].index(max(counts_of_outcomes_Pregnancies[0])))

    
    elif i >= -4.5 and i <-4:
        y_pred.append(counts_of_outcomes_Pregnancies[1].index(max(counts_of_outcomes_Pregnancies[1])))

    
    elif i >= -4 and i <-3.5:
        y_pred.append(counts_of_outcomes_Pregnancies[2].index(max(counts_of_outcomes_Pregnancies[2])))
        

    elif i >= -3.5 and i <-3:
        y_pred.append(counts_of_outcomes_Pregnancies[3].index(max(counts_of_outcomes_Pregnancies[3])))
 

    elif i >= -3 and i <-2.5:
        y_pred.append(counts_of_outcomes_Pregnancies[4].index(max(counts_of_outcomes_Pregnancies[4])))


    elif i >= -2.5 and i <-2:
        y_pred.append(counts_of_outcomes_Pregnancies[5].index(max(counts_of_outcomes_Pregnancies[5])))


    elif i >=-2 and i <-1.5:
        y_pred.append(counts_of_outcomes_Pregnancies[6].index(max(counts_of_outcomes_Pregnancies[6])))


    elif i >= -1.5 and i <-1:
        y_pred.append(counts_of_outcomes_Pregnancies[7].index(max(counts_of_outcomes_Pregnancies[7])))


    elif i >-1 and i <-0.5:
        y_pred.append(counts_of_outcomes_Pregnancies[8].index(max(counts_of_outcomes_Pregnancies[8])))
 

    elif i >= -0.5 and i <0:
        y_pred.append(counts_of_outcomes_Pregnancies[9].index(max(counts_of_outcomes_Pregnancies[9])))


    elif i >= 0 and i < 0.5:
        y_pred.append(counts_of_outcomes_Pregnancies[10].index(max(counts_of_outcomes_Pregnancies[10])))



    elif i >= 0.5 and i <1:
        y_pred.append(counts_of_outcomes_Pregnancies[11].index(max(counts_of_outcomes_Pregnancies[11])))


    elif i >= 1 and i < 1.5:
        y_pred.append(counts_of_outcomes_Pregnancies[12].index(max(counts_of_outcomes_Pregnancies[12])))


    elif i >= 1.5 and i <2:
        y_pred.append(counts_of_outcomes_Pregnancies[13].index(max(counts_of_outcomes_Pregnancies[13])))

    
    elif i >= 2 and i <2.5:
        y_pred.append(counts_of_outcomes_Pregnancies[14].index(max(counts_of_outcomes_Pregnancies[14])))

    elif i >= 2.5 and i < 3:
        y_pred.append(counts_of_outcomes_Pregnancies[15].index(max(counts_of_outcomes_Pregnancies[15])))


    elif i >= 3.5 and i <4:
        y_pred.append(counts_of_outcomes_Pregnancies[16].index(max(counts_of_outcomes_Pregnancies[16])))
   

    elif i >= 4 and i < 4.5:
        y_pred.append(counts_of_outcomes_Pregnancies[17].index(max(counts_of_outcomes_Pregnancies[17])))
        

    elif i >= 4.5 and i <5:
        y_pred.append(counts_of_outcomes_Pregnancies[18].index(max(counts_of_outcomes_Pregnancies[18])))
        

    elif i >= 5 and i <5.5:
        y_pred.append(counts_of_outcomes_Pregnancies[19].index(max(counts_of_outcomes_Pregnancies[19])))
        

    elif i >= 5.5 and i <6:
       
        y_pred.append(counts_of_outcomes_Pregnancies[20].index(max(counts_of_outcomes_Pregnancies[20])))

    elif i >= 6 and i <6.5:
        y_pred.append(counts_of_outcomes_Pregnancies[21].index(max(counts_of_outcomes_Pregnancies[21])))
       

    elif i >= 6.5 and i <7:
        y_pred.append(counts_of_outcomes_Pregnancies[22].index(max(counts_of_outcomes_Pregnancies[22])))
        

    elif i >= 7 and i <7.5:
       
        y_pred.append(counts_of_outcomes_Pregnancies[23].index(max(counts_of_outcomes_Pregnancies[23])))

    elif i >= 7.5 and i <8:
        y_pred.append(counts_of_outcomes_Pregnancies[24].index(max(counts_of_outcomes_Pregnancies[24])))
        
y_pred

from sklearn.metrics import accuracy_score

print(accuracy_score(y_pred, y_test))

# we can apply a similar procedure for other features as well. 
counts_of_outcomes_glucose = [[0,0] for i in range(25)]

for i in range(len(X_train_scaled)):

    if X_train_scaled[i][1] < -5 or X_train_scaled[i][1] > 8:
        continue

    elif X_train_scaled[i][1] >= -5 and X_train_scaled[i][1] <-4.5:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[0][1]+=1
        else:
            counts_of_outcomes_glucose[0][0]+=1
    
    elif X_train_scaled[i][1] >= -4.5 and X_train_scaled[i][1] <-4:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[1][1]+=1
        else:
            counts_of_outcomes_glucose[1][0]+=1
 
    
    elif X_train_scaled[i][1] >= -4 and X_train_scaled[i][1] <-3.5:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[2][1]+=1
        else:
            counts_of_outcomes_glucose[2][0]+=1
        

    elif X_train_scaled[i][1] >= -3.5 and X_train_scaled[i][1] <-3:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[3][1]+=1
        else:
            counts_of_outcomes_glucose[3][0]+=1
        freq_by_bins_glucose[3] += 1 

    elif X_train_scaled[i][1] >= -3 and X_train_scaled[i][1] <-2.5:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[4][1]+=1
        else:
            counts_of_outcomes_glucose[4][0]+=1
     

    elif X_train_scaled[i][1] >= -2.5 and X_train_scaled[i][1] <-2:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[5][1]+=1
        else:
            counts_of_outcomes_glucose[5][0]+=1
       


    elif X_train_scaled[i][1] >=-2 and X_train_scaled[i][1] <-1.5:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[6][1]+=1
        else:
            counts_of_outcomes_glucose[6][0]+=1
        

    elif X_train_scaled[i][1] >= -1.5 and X_train_scaled[i][1] <-1:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[7][1]+=1
        else:
            counts_of_outcomes_glucose[7][0]+=1
         

    elif X_train_scaled[i][1] >-1 and X_train_scaled[i][1] <-0.5:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[8][1]+=1
        else:
            counts_of_outcomes_glucose[8][0]+=1
    

    elif X_train_scaled[i][1] >= -0.5 and X_train_scaled[i][1] <0:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[9][1]+=1
        else:
            counts_of_outcomes_glucose[9][0]+=1
        

    elif X_train_scaled[i][1] >= 0 and X_train_scaled[i][1] < 0.5:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[10][1]+=1
        else:
            counts_of_outcomes_glucose[10][0]+=1
        

    elif X_train_scaled[i][1] >= 0.5 and X_train_scaled[i][1] <1:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[11][1]+=1
        else:
            counts_of_outcomes_glucose[11][0]+=1
        

    elif X_train_scaled[i][1] >= 1 and X_train_scaled[i][1] < 1.5:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[12][1]+=1
        else:
            counts_of_outcomes_glucose[12][0]+=1
        
    elif X_train_scaled[i][1] >= 1.5 and X_train_scaled[i][1] <2:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[13][1]+=1
        else:
            counts_of_outcomes_glucose[13][0]+=1
        
    
    elif X_train_scaled[i][1] >= 2 and X_train_scaled[i][1] <2.5:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[14][1]+=1
        else:
            counts_of_outcomes_glucose[14][0]+=1
       

    elif X_train_scaled[i][1] >= 2.5 and X_train_scaled[i][1] < 3:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[15][1]+=1
        else:
            counts_of_outcomes_glucose[15][0]+=1
        

    elif X_train_scaled[i][1] >= 3.5 and X_train_scaled[i][1] <4:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[16][1]+=1
        else:
            counts_of_outcomes_glucose[16][0]+=1
        

    elif X_train_scaled[i][1] >= 4 and X_train_scaled[i][1] < 4.5:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[17][1]+=1
        else:
            counts_of_outcomes_glucose[17][0]+=1
       

    elif X_train_scaled[i][1] >= 4.5 and X_train_scaled[i][1] <5:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[18][1]+=1
        else:
            counts_of_outcomes_glucose[18][0]+=1
      

    elif X_train_scaled[i][1] >= 5 and X_train_scaled[i][1] <5.5:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[19][1]+=1
        else:
            counts_of_outcomes_glucose[19][0]+=1
      
    elif X_train_scaled[i][1] >= 5.5 and X_train_scaled[i][1] <6:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[20][1]+=1
        else:
            counts_of_outcomes_glucose[20][0]+=1
      

    elif X_train_scaled[i][1] >= 6 and X_train_scaled[i][1] <6.5:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[21][1]+=1
        else:
            counts_of_outcomes_glucose[21][0]+=1
       

    elif X_train_scaled[i][1] >= 6.5 and X_train_scaled[i][1] <7:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[22][1]+=1
        else:
            counts_of_outcomes_glucose[22][0]+=1
      
    elif X_train_scaled[i][1] >= 7 and X_train_scaled[i][1] <7.5:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[23][1]+=1
        else:
            counts_of_outcomes_glucose[23][0]+=1
        

    elif X_train_scaled[i][1] >= 7.5 and X_train_scaled[i][1] <8:
        if y_train[i] == 1:
            counts_of_outcomes_glucose[24][1]+=1
        else:
            counts_of_outcomes_glucose[24][0]+=1

# now for each test_sample we use pregnancy to see whether it gives a good prediction or not.
y_pred1 = []
for i in X_test_scaled[:,1]:

    if i >= -5 and i <-4.5:
        y_pred1.append(counts_of_outcomes_glucose[0].index(max(counts_of_outcomes_glucose[0])))

    
    elif i >= -4.5 and i <-4:
        y_pred1.append(counts_of_outcomes_glucose[1].index(max(counts_of_outcomes_glucose[1])))

    
    elif i >= -4 and i <-3.5:
        y_pred1.append(counts_of_outcomes_glucose[2].index(max(counts_of_outcomes_glucose[2])))
        

    elif i >= -3.5 and i <-3:
        y_pred1.append(counts_of_outcomes_glucose[3].index(max(counts_of_outcomes_glucose[3])))
 

    elif i >= -3 and i <-2.5:
        y_pred1.append(counts_of_outcomes_glucose[4].index(max(counts_of_outcomes_glucose[4])))


    elif i >= -2.5 and i <-2:
        y_pred1.append(counts_of_outcomes_glucose[5].index(max(counts_of_outcomes_glucose[5])))


    elif i >=-2 and i <-1.5:
        y_pred1.append(counts_of_outcomes_glucose[6].index(max(counts_of_outcomes_glucose[6])))


    elif i >= -1.5 and i <-1:
        y_pred1.append(counts_of_outcomes_glucose[7].index(max(counts_of_outcomes_glucose[7])))


    elif i >-1 and i <-0.5:
        y_pred1.append(counts_of_outcomes_glucose[8].index(max(counts_of_outcomes_glucose[8])))
 

    elif i >= -0.5 and i <0:
        y_pred1.append(counts_of_outcomes_glucose[9].index(max(counts_of_outcomes_glucose[9])))


    elif i >= 0 and i < 0.5:
        y_pred1.append(counts_of_outcomes_glucose[10].index(max(counts_of_outcomes_glucose[10])))



    elif i >= 0.5 and i <1:
        y_pred1.append(counts_of_outcomes_glucose[11].index(max(counts_of_outcomes_glucose[11])))


    elif i >= 1 and i < 1.5:
        y_pred1.append(counts_of_outcomes_glucose[12].index(max(counts_of_outcomes_glucose[12])))


    elif i >= 1.5 and i <2:
        y_pred1.append(counts_of_outcomes_glucose[13].index(max(counts_of_outcomes_glucose[13])))

    
    elif i >= 2 and i <2.5:
        y_pred1.append(counts_of_outcomes_glucose[14].index(max(counts_of_outcomes_glucose[14])))

    elif i >= 2.5 and i < 3:
        y_pred1.append(counts_of_outcomes_glucose[15].index(max(counts_of_outcomes_glucose[15])))


    elif i >= 3.5 and i <4:
        y_pred1.append(counts_of_outcomes_glucose[16].index(max(counts_of_outcomes_glucose[16])))
   

    elif i >= 4 and i < 4.5:
        y_pred1.append(counts_of_outcomes_glucose[17].index(max(counts_of_outcomes_glucose[17])))
        

    elif i >= 4.5 and i <5:
        y_pred1.append(counts_of_outcomes_glucose[18].index(max(counts_of_outcomes_glucose[18])))
        

    elif i >= 5 and i <5.5:
        y_pred1.append(counts_of_outcomes_glucose[19].index(max(counts_of_outcomes_glucose[19])))
        

    elif i >= 5.5 and i <6:
       
        y_pred1.append(counts_of_outcomes_glucose[20].index(max(counts_of_outcomes_glucose[20])))

    elif i >= 6 and i <6.5:
        y_pred1.append(counts_of_outcomes_glucose[21].index(max(counts_of_outcomes_glucose[21])))
       

    elif i >= 6.5 and i <7:
        y_pred1.append(counts_of_outcomes_glucose[22].index(max(counts_of_outcomes_glucose[22])))
        

    elif i >= 7 and i <7.5:
       
        y_pred1.append(counts_of_outcomes_glucose[23].index(max(counts_of_outcomes_glucose[23])))

    elif i >= 7.5 and i <8:
        y_pred1.append(counts_of_outcomes_glucose[24].index(max(counts_of_outcomes_glucose[24])))
        
y_pred1

from sklearn.metrics import accuracy_score

print(accuracy_score(y_pred1, y_test))

# similarly the same can be applied for the other features as well
