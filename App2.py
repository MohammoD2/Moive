import streamlit as st
import pandas as pd
import pickle
import requests 
import joblib
st.title('Welcome To Ibrahim Creation ')
st.header('Creator- Mohammod Ibrahim Hossain ')
# st.image('My profressional photos.jpg',caption="Creator")
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def recomnetion(movie):
    movies_index = moives[moives['title'] == movie].index[0]
    distance = similarity[movies_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    movie_titles = [] 
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = moives.iloc[i[0]].movie_id

        recommended_movie_posters.append(fetch_poster(movie_id))
        movie_titles.append(moives.iloc[i[0]].title)  # Append to movie_titles list
    return recommended_movie_posters ,movie_titles
st.title("Movie Recommendation System")
model_path="/mount/src/movie/Movie_dict1.pkl"
movies_dict = joblib.load(model_path)
moives = pd.DataFrame(movies_dict)

similarity_t = "/mount/src/Movie/similarity1.pkl"
similarity =joblib.load(similarity_t)
selected_movie_name = st.selectbox(
    'Select a movie:',
    moives['title'].values)

if st.button('Show Recommendations'):
    recommended_movie_posters, recommended_movie_titles = recomnetion(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_titles[0])
        st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movie_titles[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_titles[2])
        st.image(recommended_movie_posters[2])

    with col4:
        st.text(recommended_movie_titles[3])
        st.image(recommended_movie_posters[3])

    with col5:
        st.text(recommended_movie_titles[4])
        st.image(recommended_movie_posters[4])