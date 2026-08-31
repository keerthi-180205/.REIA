import streamlit as st

st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 House Price Prediction")
st.write("""
Welcome to the House Price Prediction application!

This application uses Machine Learning to estimate the price of a property
based on various features such as location, property type, number of bedrooms,
bathrooms, built-up area, furnishing type, and other property details.
""")

st.divider()

st.subheader("How it works")

st.write("""
1. Go to the **Price Prediction** page.
2. Enter the property details.
3. Click the **Predict Price** button.
4. Get the estimated property price.
""")

st.divider()

st.subheader("Features Used")

col1, col2 = st.columns(2)

with col1:
    st.write("""
    - Property Type
    - Sector
    - Bedrooms
    - Bathrooms
    - Balcony
    - Age Possession
    """)

with col2:
    st.write("""
    - Built-up Area
    - Servant Room
    - Store Room
    - Furnishing Type
    - Luxury Category
    - Floor Category
    """)