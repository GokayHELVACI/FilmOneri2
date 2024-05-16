from flask import Flask, request, jsonify, render_template
import pandas as pd
import random
import similar_movies

app = Flask(__name__)

defaultPage='/index.html'


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
    secilen_filmler = en_yuksek_puanli_filmler('test.csv', 5000)  # Örneğin 5 film seçelim
    print('vallaha calisiyom')
    # Seçilen filmlerin bilgilerini içeren bir liste oluştur
    filmler = []
    for index, row in secilen_filmler.iterrows():
        film_bilgisi = {
            'ad': row['title'],
            'turu': row['genres'],
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
    
    return_val = 'Film Adi:' + film_ad + ' <br>  Benzerleri: ' + ','.join(films.values)
    return return_val



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
