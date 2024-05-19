from flask import Flask, request, jsonify, render_template
import pandas as pd
import random
import similar_movies
import json


import requests
from bs4 import BeautifulSoup

import requests
from PIL import Image
import requests
from io import BytesIO
from collections import Counter
import time
import numpy as np

def dominant_color(url):
    start = time.time()
    response = requests.get(url)
    print("Çalışma Süresi:", time.time() - start)

    image = Image.open(BytesIO(response.content))
    image = image.convert('RGB')

    # Pixelleri al ve numpy array'e çevir
    pixels = np.array(image)

    # Piksel ortalamasını hesapla
    average_color = np.mean(pixels, axis=(0, 1)).astype(int)
    return average_color

url = 'https://media.themoviedb.org/t/p/original/drw6bZFRP1Yv5LNFW0KLoAgWo5.jpg'
dominant_rgb = dominant_color(url)
print(f"En baskın renk (RGB): {dominant_rgb}")


def get_movie_image(film_ad):
    api_key = '9ae4aa8fd098519b71e941c397067bc3'

    # Make the request
    url = f'https://api.themoviedb.org/3/search/movie?query={film_ad}&api_key={api_key}'
    response = requests.get(url)

    return "https://media.themoviedb.org/t/p/original"+response.json()['results'][0]['backdrop_path']

print(get_movie_image("godzilla"))


app = Flask(__name__)
using_dataset='tmdb_5000_movies.csv'
defaultPage='/index.html'
redirectedPage ='/test.html'

def en_yuksek_puanli_filmler(csv_dosya, film_sayisi):
    # CSV dosyasını pandas ile oku
    df = pd.read_csv(csv_dosya)
    
    # 'vote_average' sütununa göre DataFrame'i sırala ve en yüksek puan alan filmleri seç
    en_yuksek_puanli_filmler = df.sort_values(by='vote_average', ascending=False).head(film_sayisi)
    
    return en_yuksek_puanli_filmler

@app.route('/')
def index():
    # Belirtilen sayıda rastgele filmi seç
    print('vallaha calisiyom')
    secilen_filmler = en_yuksek_puanli_filmler(using_dataset, 50)  # Örneğin 5 film seçelim
    print('vallaha calisiyom')
    # Seçilen filmlerin bilgilerini içeren bir liste oluştur
    filmler = []
    for index, row in secilen_filmler.iterrows():
        genres = json.loads(row['genres'])
        genre_names = [genre['name'] for genre in genres]
        genre_string = ', '.join(genre_names)
        film_bilgisi = {
            'ad': row['title'],
            'turu': genre_string,
            #'turu': row['genres'], #test.csv de bu şekilde kullan 
            'puan': row['vote_average']
        }
        filmler.append(film_bilgisi)
    print(filmler)
    # Seçilen filmlerin bilgilerini HTML içeriği olarak render_template fonksiyonuna ileterek, belirli bir HTML dosyasını kullanabiliriz
    return render_template('index.html', filmler=filmler)


@app.route('/film_detay/<film_ad>', methods=['GET', 'POST'])
def film_detay(film_ad):
    if request.method == 'POST':
        # Eğer POST isteği yapıldıysa
        print('POST isteği yapıldı')
    else:
        films, scores = similar_movies.get_similar_movies(film_ad)

        # Eğer GET isteği yapıldıysa
        print('GET isteği yapıldı')
    print('Selam',films.values)
    image_url = get_movie_image(film_ad)
    dominant_color_on_html=dominant_color(image_url)
    return render_template('test.html', similar_movies=films.values , main_movie=film_ad, image_url=image_url,dominant_color="rgb("+str(dominant_color_on_html[0])+" "+str(dominant_color_on_html[1])+" "+str(dominant_color_on_html[2])+" / 50% )")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
