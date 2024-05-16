import csv
import pandas as pd
from sklearn.model_selection import  train_test_split
from sklearn.linear_model import LinearRegression

# Veri setinde 1011958 satir 24 sutundan olusmakta #
# dataset = "TMDB_movie_dataset_v11.csv" #


dataset = "test.csv"
 
file = open(dataset,"r",encoding="utf8")
data = list(csv.reader(file,delimiter=","))
file.close()

df = pd.read_csv(dataset)
    #df = df[df['type'].str.contains('Movie')] # Print only movies # 
    #print(df[['title','cast']])
    #print(df[['title', 'genres']])
    #df = df[df['type'].str.contains('name')] # Print only movies # 
#print(df[['title','genre','cast']])

print(df)
