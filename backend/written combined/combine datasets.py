import pandas as pd 
import numpy as np
# from pandas import DataFrame as df

labels = [  
    '0','1','2','3','4','5','6','7','8','9',
    'A','B','C','D','E','F','G','H','I','J',
    'K','L','M','N','O','P','Q','R','S','T',
    'U','V','W','X','Y','Z']


directory = "backend/training/"

digitsData = pd.read_csv("backend/training/0_9 Handwritten Data.csv").astype('float32')
lettersData = pd.read_csv("backend/training/A_Z Handwritten Data.csv").astype('float32')

df = lettersData
# df.rename(columns={'0':'label'}, inplace=True)

numbers_0_25 = [i for i in range(0, 26)]
numbers_10_35 = [i for i in range(10, 36)]

df.iloc[:, 0] = df.iloc[:, 0].replace(numbers_0_25,numbers_10_35)

df.columns = digitsData.columns
newDf = pd.concat([digitsData,df])
print(df.shape, digitsData.shape)
# newDf = digitsData.append(df)
# newDf = digitsData + df
print(newDf)


# 4. Save list of lists to CSV
newDf.to_csv("backend/training/combinedHandWritten.csv", index=False)
