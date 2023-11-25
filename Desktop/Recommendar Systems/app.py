import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similar = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    try:
        data = requests.get(url)
        data.raise_for_status() # Check for errors
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading movie info: {e}")
        return None

def recommend ( movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Movie not found. Please choose another movie.")
        return [], []
    index=movie_index
    distances = similar[movie_index]
    movie_list = sorted(list(enumerate(similar[index])), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # retrieve the poster from the API
        poster_path = fetch_poster(movie_id)
        if poster_path:
            recommended_movies_posters.append(poster_path)

    return recommended_movies, recommended_movies_posters

# Stream the layout
st.title('Movie Recommender System')
option = st.selectbox('Select a movie', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend (option)

    # Display selected movie information
    selected_movie = movies[movies['title'] == option].iloc[0]
    st.write(f"**Selected movie:** {selected_movie['title']}")
    # Show recommended movies
    column1, column2, column3, column4, column5 = st.columns(5)
    with column1:
        st.text(names[0])
        st.image(posters[0], use_column_width=True)
    with column2:
        st.text(names[1])
        st.image(posters[1], use_column_width=True)
    with column3:
        st.text(names[2])
        st.image(posters[2], use_column_width=True)
    with column4:
        st.text(names[3])
        st.image(posters[3], use_column_width=True)
    with column5:
        st.text(names[4])
        st.image(posters[4], use_column_width=True)