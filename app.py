import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack

# Load the dataset
data = pd.read_csv('recipe_final (1).csv')

# Preprocess the ingredients and numerical data
vectorizer = TfidfVectorizer()
X_ingredients = vectorizer.fit_transform(data['ingredients_list'])

scaler = StandardScaler()   
X_numerical = scaler.fit_transform(data[['calories', 'fat', 'carbohydrates', 'protein', 'cholesterol', 'sodium', 'fiber']])

# Combine numerical and ingredient features using scipy's hstack to keep it sparse
X_combined = hstack([X_numerical, X_ingredients])

# Train the KNN model
knn = NearestNeighbors(n_neighbors=3, metric='euclidean')
knn.fit(X_combined)

# Define the recommendation function
def recommend_recipe(input_features):
    input_features_scaled = scaler.transform([input_features[:7]])  # Scale the input features
    input_ingredients_transformed = vectorizer.transform([input_features[7]])  # Transform the input ingredients
    input_combined = hstack([input_features_scaled, input_ingredients_transformed])  # Keep input sparse
    distances, indices = knn.kneighbors(input_combined)  # Get the indices of the nearest neighbors
    recommendation = data.iloc[indices[0]]  # Get the recommendations
    return recommendation[['recipe_name', 'ingredients_list', 'image_url']]  # Return the recommendations

# Streamlit App Configuration
st.set_page_config(
    page_title="Recipe Recommendation App",
    page_icon="🏡",
    layout="wide",  # Wide layout
    initial_sidebar_state="expanded",
)

# Apply CSS for uniform image size and centering
st.markdown(
    """
    <style>
    .recipe-image {
        width: 200px;
        height: 200px;
        object-fit: cover;
        margin: auto;
    }
    .recipe-name {
        text-align: center;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
    }
    .st-expander {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True
)

# Menu
selected = option_menu(
    menu_title=None,
    options=["Home", "App", "Contact"],
    icons=["house", "book", "envelope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {
            "font-size": "25px",
            "text-align": "left",
            "margin": "0px",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "green"},
    },
)

# Home Page
if selected == "Home":
    st.title('Welcome to the Recipe Recommendation App')
    st.image("recipe.png")

# App Page
elif selected == "App":
    st.title('Recipe Recommendation App')

    # Input Form
    col1, col2 = st.columns(2)
    with col1:
        calories = st.number_input('Calories', min_value=0)
        fat = st.number_input('Fat (g)', min_value=0)
        carbohydrates = st.number_input('Carbohydrates (g)', min_value=0)
        protein = st.number_input('Protein (g)', min_value=0)

    with col2:
        cholesterol = st.number_input('Cholesterol (mg)', min_value=0)
        sodium = st.number_input('Sodium (mg)', min_value=0)
        fiber = st.number_input('Fiber (g)', min_value=0)
        ingredients = st.text_input('Ingredients (comma-separated)', 'chicken, rice, salt, pepper, onion, garlic')

    input_features = [calories, fat, carbohydrates, protein, cholesterol, sodium, fiber, ingredients]

    if st.button('Recommend'):
        recommendations = recommend_recipe(input_features)

        if not recommendations.empty:
            st.write("Here are the recommended recipes:")

            # Create a row of columns for the images, ensuring 3 boxes per row
            cols = st.columns(3)

            for i, (index, row) in enumerate(recommendations.iterrows()):
                with cols[i % 3]:  # Use modulus to cycle through columns
                    # Display the recipe name first and center it using CSS
                    st.markdown(
                        f"""
                        <div class="recipe-name">{row['recipe_name']}</div>
                        """, unsafe_allow_html=True
                    )

                    # Use a div for image display to apply custom CSS
                    st.markdown(
                        f"""
                        <div style="text-align:center;">
                            <img class="recipe-image" src="{row['image_url']}" />
                        </div>
                        """, unsafe_allow_html=True
                    )
                    
                    with st.expander("Ingredients"):
                        st.write(f"Ingredients: {row['ingredients_list']}")

        else:
            st.write("No recommendations found for the given input.")

# Contact Page
elif selected == "Contact":
    st.write("##### About the author:")
    st.write("<p style='color:blue; font-size: 50px; font-weight: bold;'>Usama Munawar</p>", unsafe_allow_html=True)
    st.write("##### Connect with me on social media")

    linkedin_url = "https://img.icons8.com/color/48/000000/linkedin.png"
    github_url = "https://img.icons8.com/fluent/48/000000/github.png"
    youtube_url = "https://img.icons8.com/?size=50&id=19318&format=png"
    twitter_url = "https://img.icons8.com/color/48/000000/twitter.png"
    facebook_url = "https://img.icons8.com/color/48/000000/facebook-new.png"

    linkedin_redirect_url = "https://www.linkedin.com/in/abu--usama"
    github_redirect_url = "https://github.com/UsamaMunawarr"
    youtube_redirect_url = "https://www.youtube.com/@CodeBaseStats"
    twitter_redirect_url = "https://twitter.com/Usama__Munawar?t=Wk-zJ88ybkEhYJpWMbMheg&s=09"
    facebook_redirect_url = "https://www.facebook.com/profile.php?id=100005320726463&mibextid=9R9pXO"

    st.markdown(f'<a href="{github_redirect_url}"><img src="{github_url}" width="60" height="60"></a>'
                f'<a href="{linkedin_redirect_url}"><img src="{linkedin_url}" width="60" height="60"></a>'
                f'<a href="{youtube_redirect_url}"><img src="{youtube_url}" width="60" height="60"></a>'
                f'<a href="{twitter_redirect_url}"><img src="{twitter_url}" width="60" height="60"></a>'
                f'<a href="{facebook_redirect_url}"><img src="{facebook_url}" width="60" height="60"></a>', unsafe_allow_html=True)

# Thank you message
st.write("<p style='color:green; font-size: 30px; font-weight: bold;'>Thank you for using this app, share with your friends!😇</p>", unsafe_allow_html=True)
