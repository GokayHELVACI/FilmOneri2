import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse as sp
from sklearn.preprocessing import MinMaxScaler
import re
import time
# Veri kümesini yükle


start_time = time.time()
scaler = MinMaxScaler()

df = pd.read_csv('tmdb_5000_movies.csv')

df['release_date'] = pd.to_datetime(df['release_date'])
df['release_year'] = df['release_date'].dt.year
df['release_month'] = df['release_date'].dt.month
df['release_day'] = df['release_date'].dt.day

# Metinsel sütunları seç
text_columns = ['genres', 'keywords', 'original_language', 'original_title', 'overview', 'production_companies', 'production_countries', 'spoken_languages', 'status', 'tagline', 'title']

# Eksik değerleri doldur
df[text_columns] = df[text_columns].fillna('')

# Metinsel sütunları birleştir
df['combined_text'] = df[text_columns].apply(lambda x: ' '.join(x), axis=1)
df['combined_text'] = df['combined_text'].apply(lambda x: re.sub(r'[^\w\s]', '', x))

# TF-IDF vektörizasyonu
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined_text'])

# Sayısal sütunları seç
numerical_columns = ['budget', 'revenue', 'popularity', 'runtime', 'vote_average', 'vote_count', 'release_year']
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
df[numerical_columns] = df[numerical_columns].fillna(0)

numerical_data = df[numerical_columns].values

# Sayısal ve metinsel verileri birleştir
combined_data = sp.hstack((numerical_data.astype(float), tfidf_matrix))


# Benzerlik matrisini hesapla
cosine_sim = cosine_similarity(combined_data, combined_data)

# Öneri yapmak için fonksiyon
def get_recommendations(title, cosine_sim=cosine_sim):
    # Film başlığına göre index'i al
    idx = df[df['title'] == title].index[0]
    # Tüm filmlerin benzerlik skorunu al
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Benzerlik skorlarına göre sırala
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # En benzer 10 filmi al
    sim_scores = sim_scores[1:11]
    # Benzer filmlerin index'lerini al
    movie_indices = [i[0] for i in sim_scores]
    # Benzer filmlerin başlıklarını ve benzerlik skorlarını döndür
    return df['title'].iloc[movie_indices], [i[1] for i in sim_scores]


def  get_similar_movies(film_adi):




    # Örnek kullanım

    movie_title = film_adi

    recommendations, scores = get_recommendations(movie_title)

    for movie, score in zip(recommendations, scores):
        print(f'{movie}: {score}')
        
        
        
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Kodun çalışma süresi: {execution_time} saniye")
    
    return recommendations, scores