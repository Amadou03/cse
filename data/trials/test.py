import pandas as pd
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
df=pd.read_csv('data1.csv')
print(df)