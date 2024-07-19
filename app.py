from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import requests

app = Flask(__name__)

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/')
def index():
    movie_titles = movies['title'].values
    return render_template('index.html', movie_titles=movie_titles)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    movie = request.form['movie']
    names, posters = recommend(movie)
    return jsonify({'names': names, 'posters': posters})

if __name__ == '__main__':
    app.run(debug=True)
