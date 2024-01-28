import streamlit as st
import pandas as pd
import requests
import joblib

# Load configuration from the dictionary
title = app_config["title"]
creator = app_config["creator"]
model_path = app_config["model_path"]
similarity_path = app_config["similarity_path"]
poster_api_key = app_config["poster_api_key"]
poster_base_url = app_config["poster_base_url"]
poster_image_url = app_config["poster_image_url"]
num_recommendations = app_config["num_recommendations"]

st.title(title)
st.header(f"Creator- {creator}")

def fetch_poster(movie_id):
    url = poster_base_url.format(movie_id, poster_api_key)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = poster_image_url.format(poster_path)
    return full_path

def recommendation(movie):
    movies_index = movies_df[movies_df['title'] == movie].index[0]
    distance = similarity_matrix[movies_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:num_recommendations + 1]
    movie_titles = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        movie_titles.append(movies_df.iloc[i[0]].title)

    return recommended_movie_posters, movie_titles

# Load data and model
movies_df = pd.DataFrame(joblib.load(model_path))
similarity_matrix = joblib.load(similarity_path)

selected_movie_name = st.selectbox('Select a movie:', movies_df['title'].values)

if st.button('Show Recommendations'):
    recommended_movie_posters, recommended_movie_titles = recommendation(selected_movie_name)

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
