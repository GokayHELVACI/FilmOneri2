import csv
import pandas as pd
from sklearn.model_selection import  train_test_split
from sklearn.linear_model import LinearRegression
import json

# Veri setinde 1011958 satir 24 sutundan olusmakta #
# dataset = "TMDB_movie_dataset_v11.csv" #


dataset = "tmdb_5000_movies.csv"
 
file = open(dataset,"r",encoding="utf8")
data = list(csv.reader(file,delimiter=","))
#file.close()

df = pd.read_csv(dataset)
    #df = df[df['type'].str.contains('Movie')] # Print only movies # 
    #print(df[['title','cast']])
    #print(df[['title', 'genres']])
    #df = df[df['type'].str.contains('name')] # Print only movies # 
#print(df[['title','genre','cast']])

#print(df['genres'])

import csv
import json

# CSV dosyasını okuma
# with open(dataset, 'r', encoding='utf-8') as file:
#     reader = csv.DictReader(file)
    
#     # Her satır için işlemleri yapma
#     for row in reader:
#         # "genres" sütunundaki JSON verisini ayrıştırma
#         genres = json.loads(row['genres'].replace('""', '"'))
        
#         # Türleri yazdırma
#         genre_names = [genre['name'] for genre in genres]
#         print(f"Film: {row['title']}")
#         print("Türler: ", ", ".join(genre_names))


import csv
import json

def extract_genres_from_csv(file_path):
    genres_output = []
    
    # CSV dosyasını okuma
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Her satır için işlemleri yapma
        for row in reader:
            # "genres" sütunundaki JSON verisini ayrıştırma
            genres = json.loads(row['genres'].replace('""', '"'))
            
            # Türleri bir listeye ekleme
            genre_names = [genre['name'] for genre in genres]
            genres_output.append(f"Film: {row['title']}\nTürler: {', '.join(genre_names)}\n")
    
    return genres_output

# Fonksiyonu çağırma ve çıktıyı bir değişkene atama
file_path = 'tmdb_5000_movies.csv'
genres_list = extract_genres_from_csv(file_path)

# Çıktıyı yazdırma
for genres in genres_list:
    print(genres)

