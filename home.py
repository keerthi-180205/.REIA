import streamlit as st

st.set_page_config(
    page_title="Gurgaon Real Estate Hub",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Gurgaon Real Estate Hub")

st.markdown("""
Welcome to the **Gurgaon Real Estate Hub** — a Machine Learning-powered web app to help you
explore, predict, and discover properties in the Gurgaon market.

Navigate through the pages in the sidebar to get started.
""")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔮 Price Prediction")
    st.write(
        "Enter property details like sector, BHK, built-up area, furnishing, and more "
        "to get an AI-estimated price range."
    )

with col2:
    st.subheader("📊 Analytics Dashboard")
    st.write(
        "Explore an interactive geo-price map, feature word clouds, area vs price plots, "
        "BHK pie charts, and price distribution graphs."
    )

with col3:
    st.subheader("🏢 Recommend Apartments")
    st.write(
        "Search apartments within a radius of your chosen location and find the "
        "top 5 geographically similar properties."
    )

st.markdown("---")

st.info("👈 Use the sidebar to navigate between pages.")
