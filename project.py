import pandas as pd

df = pd.read_csv('weatherAUS.csv')

df.isnull().sum()
(df.isnull().sum() / len(df)) * 100