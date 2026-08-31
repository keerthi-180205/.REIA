# 🏠 House Price Prediction & Analytics

Welcome to the **House Price Prediction & Analytics** application! This project is a comprehensive Machine Learning and Data Visualization web app built with Streamlit. It is designed to help users estimate property prices, explore deep real estate analytics, and discover similar apartments based on geographical proximity and property features, specifically focusing on the Gurgaon real estate market.

## ✨ Key Features

### 1. 🔮 Price Prediction
- **Machine Learning Estimation:** Accurately estimates property prices based on multiple features.
- **Input Parameters:** Location (Sector), Property Type (House/Flat), Bedrooms, Bathrooms, Balcony, Age of Possession, Built-up Area, Servant Room, Store Room, Furnishing Type, Luxury Category, and Floor Category.

### 2. 📊 Analytics Dashboard
An interactive dashboard providing deep insights into the real estate market:
- **Interactive Price Map:** A geographic map (using Folium) centered on Gurgaon, showing average prices, price per sqft, and built-up areas by sector with a dynamic color scale.
- **Feature Word Clouds:** Dynamic word clouds that display the most common property features. It can be filtered by specific sectors by clicking on the interactive map!
- **Area vs. Price Analysis:** Interactive scatter plots comparing built-up area and price, categorized by property type (House vs. Flat).
- **BHK Distribution:** Pie charts illustrating the distribution of BHKs (Bedrooms, Hall, Kitchen), filterable by sector.
- **Price Comparisons:** Box plots for side-by-side BHK price comparisons across different sectors.
- **Price Distribution:** Density plots comparing the price distributions of houses versus flats.

### 3. 🏢 Apartment Recommendations
- **Geographical Proximity:** Select an apartment and instantly find the top 5 most similar apartments located geographically closest to your selection.
- **Euclidean Distance Matching:** Uses Euclidean distance algorithms to accurately recommend properties based on precise geographic coordinates and specific attributes rather than just price.

## 🛠️ Technology Stack
- **Web Framework:** [Streamlit](https://streamlit.io/)
- **Data Manipulation:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn
- **Data Visualization:** Plotly Express, Seaborn, Matplotlib, WordCloud
- **Geospatial Mapping:** Folium, Streamlit-Folium, Branca

## 🚀 Installation & Setup

1. **Clone the repository** (if pushed to GitHub):
   ```bash
   git clone <your-repository-url>
   cd <your-repository-directory>
   ```

2. **Create a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the requirements:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 How to Use

1. Run the Streamlit application from your terminal:
   ```bash
   streamlit run Home.py
   ```
2. Navigate through the sidebar to explore different pages:
   - **Home (Price Prediction):** Enter property details to get an estimated price.
   - **Recommend Apartments:** Choose a property to get geographical and feature-based recommendations.
   - **Analytics:** Explore interactive charts, maps, and word clouds to understand market trends.
