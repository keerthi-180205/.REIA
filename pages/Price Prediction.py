from sklearn import pipeline
import streamlit as st
import pickle 
import numpy as np 
import pandas as pd
import os

# Get the absolute path of the directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct paths relative to the current script's directory
df_path = os.path.join(current_dir, "..", "df.pkl")
pipeline_path = os.path.join(current_dir, "..", "notebook", "pipeline.pkl")

with open(df_path, "rb") as f:
    df = pickle.load(f)

with open(pipeline_path, "rb") as f:
    pipeline = pickle.load(f)

st.header("Enter your inputs : ")

col1, col2 = st.columns(2)

with col1:
    property_type = st.selectbox(
        "Property Type", ['flat','house']
    )

with col2:
    sector = st.selectbox(
        "Sector", df['sector'].unique()
    )


col1, col2 = st.columns(2)

with col1:
    bedrooms = st.selectbox(
        "Bedrooms",
        sorted(df['bedRoom'].unique())
    )

with col2:
    bathrooms = st.selectbox(
        "Bathrooms",
        sorted(df['bathroom'].unique())
    )

col1, col2 = st.columns(2)

with col1:
    balcony = st.selectbox(
        "Balconies",
        sorted(df['balcony'].unique())
    )

with col2:
    property_age = st.selectbox(
        "Property Age",
        sorted(df['agePossession'].unique())
    )

col1, col2 = st.columns(2)

with col1:
    built_up_area = float(
        st.number_input("Built Up Area (sqft)")
    )

with col2:
    servant_room = st.selectbox(
        "Servant Room",
        ["No", "Yes"]
    )

    servant_room = 1.0 if servant_room == "Yes" else 0.0

col1, col2 = st.columns(2)

with col1:
    store_room = st.selectbox(
        "Store Room",
        ["No", "Yes"]
    )

    store_room = 1.0 if store_room == "Yes" else 0.0

with col2:
    furnishing = st.selectbox(
        "Furnishing", df['furnishing_type'].unique()
    )

col1, col2 = st.columns(2)

with col1:
    luxury_category = st.selectbox(
        "Luxury Category", df['luxury_category'].unique()
    )

with col2:
    floor_category = st.selectbox(
        "Floor Category", df['floor_category'].unique()
    )

if st.button('Predict'):


    # form a dataframe
    data = [[property_type, sector, bedrooms, bathrooms, balcony, property_age, built_up_area, servant_room, store_room, furnishing, luxury_category, floor_category]]

    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
       'agePossession', 'built_up_area', 'servant room', 'store room',
       'furnishing_type', 'luxury_category', 'floor_category']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)
    
    # prediction
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low_price = base_price - 0.25
    high_price = base_price + 0.25

    st.markdown(
    f"### 💰 Estimated Price Range: "
    f"₹{low_price:.2f} Cr – ₹{high_price:.2f} Cr"
)
