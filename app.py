from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

defaultPage='/index.html'

# Örnek film verisi
films = [
    {"title": "The Shawshank Redemption", "genre": "Drama", "rating": 9.3},
    {"title": "The Godfather", "genre": "Crime", "rating": 9.2},
    {"title": "The Dark Knight", "genre": "Action", "rating": 9.0},
    {"title": "Pulp Fiction", "genre": "Crime", "rating": 8.9},
    {"title": "Fight Club", "genre": "Drama", "rating": 8.8}
]
@app.route('/')
def hello():
    return render_template(defaultPage)
# Basit bir film önerme endpoint'i
@app.route('/recommendations', methods=['POST'])
def recommend_movies():
    req_data = request.get_json()
    genre = req_data['genre']
    min_rating = float(req_data.get('min_rating', 0))

    recommended_movies = [movie for movie in films if movie['genre'] == genre and movie['rating'] >= min_rating]

    return jsonify(recommended_movies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
