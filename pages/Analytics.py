import streamlit as st
import pandas as pd
import folium
from branca.colormap import LinearColormap
from streamlit_folium import st_folium
import pickle
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import seaborn as sns
import ast


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Analytics Dashboard",
    layout="wide"
)

st.title("Analytics Dashboard")


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

new_df = pd.read_csv(
    "data/data-viz1.csv"
)

with open("data/feature_text.pkl", "rb") as f:
    feature_text = pickle.load(f)


# --------------------------------------------------
# CONVERT COORDINATES
# --------------------------------------------------

new_df["latitude"] = pd.to_numeric(
    new_df["latitude"],
    errors="coerce"
)

new_df["longitude"] = pd.to_numeric(
    new_df["longitude"],
    errors="coerce"
)


# --------------------------------------------------
# REMOVE MISSING COORDINATES
# --------------------------------------------------

new_df = new_df.dropna(
    subset=["latitude", "longitude"]
)


# --------------------------------------------------
# GROUP SECTOR DATA
# --------------------------------------------------

group_df = (
    new_df
    .groupby("sector", as_index=False)
    .agg({
        "price": "mean",
        "price_per_sqft": "mean",
        "built_up_area": "mean",
        "latitude": "mean",
        "longitude": "mean"
    })
)


# --------------------------------------------------
# CENTER MAP ON GURGAON
# --------------------------------------------------

center_lat = group_df["latitude"].mean()
center_lon = group_df["longitude"].mean()


# --------------------------------------------------
# CREATE MAP
# --------------------------------------------------

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=12,
    tiles="OpenStreetMap"
)


# --------------------------------------------------
# CREATE PRICE COLOR SCALE
# --------------------------------------------------

colormap = LinearColormap(
    colors=["blue", "green", "yellow", "red"],
    vmin=group_df["price_per_sqft"].min(),
    vmax=group_df["price_per_sqft"].max(),
    caption="Average Price per Sqft"
)


# --------------------------------------------------
# ADD SECTOR MARKERS
# --------------------------------------------------

for _, row in group_df.iterrows():

    folium.CircleMarker(
        location=[
            row["latitude"],
            row["longitude"]
        ],

        radius=8,

        popup=f"""
        <b>{row["sector"]}</b><br>
        Average Price: ₹{row["price"]:.2f} Cr<br>
        Price per sqft: ₹{row["price_per_sqft"]:,.0f}<br>
        Built-up Area: {row["built_up_area"]:,.0f} sqft
        """,

        tooltip=row["sector"],

        color=colormap(row["price_per_sqft"]),

        fill=True,

        fill_color=colormap(row["price_per_sqft"]),

        fill_opacity=0.8

    ).add_to(m)


# --------------------------------------------------
# ADD COLOR LEGEND
# --------------------------------------------------

colormap.add_to(m)


# --------------------------------------------------
# MAP SECTION
# --------------------------------------------------

st.header("Gurgaon Properties Price Map")


# --------------------------------------------------
# CREATE SECTOR FEATURE DICTIONARY
# --------------------------------------------------

@st.cache_data
def get_sector_feature_dict():

    df = pd.read_csv(
        "data/gurgaon_properties_cleaned_v1.csv"
    )

    sector_features = {}

    for _, row in df.iterrows():

        sector = str(
            row["sector"]
        ).lower().strip()

        features = str(
            row["features"]
        )

        if (
            pd.notna(features)
            and features.strip()
            and features != "nan"
        ):

            try:

                feat_list = ast.literal_eval(
                    features
                )

                if isinstance(
                    feat_list,
                    list
                ):

                    feat_text = " ".join(
                        feat_list
                    )

                    sector_features[sector] = (
                        sector_features.get(
                            sector,
                            ""
                        )
                        + " "
                        + feat_text
                    )

            except Exception:
                pass

    return sector_features


# --------------------------------------------------
# LOAD SECTOR FEATURES
# --------------------------------------------------

sector_dict = get_sector_feature_dict()


# --------------------------------------------------
# DISPLAY MAP
# --------------------------------------------------

st_folium_out = st_folium(
    m,
    width=1200,
    height=700,
    key="gurgaon_price_map"
)


# --------------------------------------------------
# GET SELECTED SECTOR
# --------------------------------------------------

selected_sector = None

if (
    st_folium_out
    and st_folium_out.get(
        "last_object_clicked_tooltip"
    )
):

    selected_sector = (
        st_folium_out[
            "last_object_clicked_tooltip"
        ]
    )


# --------------------------------------------------
# WORD CLOUD SECTION
# --------------------------------------------------

if (
    selected_sector
    and selected_sector.lower()
    in sector_dict
    and sector_dict[
        selected_sector.lower()
    ].strip()
):

    st.header(
        f"Top Features Word Cloud for "
        f"{selected_sector.title()}"
    )

    text_to_use = (
        sector_dict[
            selected_sector.lower()
        ]
    )

else:

    if selected_sector:

        st.header(
            f"Top Features Word Cloud for "
            f"{selected_sector.title()} "
            f"(Showing All Sectors)"
        )

    else:

        st.header(
            "Top Features Word Cloud for "
            "All Sectors"
        )

    text_to_use = feature_text


# --------------------------------------------------
# HANDLE EMPTY TEXT
# --------------------------------------------------

if (
    not text_to_use
    or len(text_to_use.strip()) == 0
):

    text_to_use = "No Features Available"


# --------------------------------------------------
# GENERATE WORD CLOUD
# --------------------------------------------------

wordcloud = WordCloud(
    width=800,
    height=800,
    background_color="white",
    stopwords=set([
        "s",
        "sq",
        "ft",
        "nan"
    ]),
    min_font_size=10
).generate(
    text_to_use
)


# --------------------------------------------------
# DISPLAY WORD CLOUD
# --------------------------------------------------

fig_wordcloud, ax = plt.subplots(
    figsize=(4, 4),
    facecolor=None
)

ax.imshow(
    wordcloud,
    interpolation="bilinear"
)

ax.axis("off")

fig_wordcloud.tight_layout(
    pad=0
)

st.pyplot(
    fig_wordcloud,
    use_container_width=True
)


# --------------------------------------------------
# AREA VS PRICE GRAPH
# --------------------------------------------------

st.header(
    "Area vs Price Graph"
)

property_type = st.selectbox(
    "Select Property Type",
    options=new_df[
        "property_type"
    ].unique(),
    key="property_type_select"
)


if property_type == "house":

    fig_area_price = px.scatter(

        new_df[
            new_df["property_type"]
            == "house"
        ],

        x="built_up_area",

        y="price",

        color="bedRoom",

        title="Area Vs Price",

        render_mode="svg"
    )

else:

    fig_area_price = px.scatter(

        new_df[
            new_df["property_type"]
            == "flat"
        ],

        x="built_up_area",

        y="price",

        color="bedRoom",

        title="Area Vs Price",

        render_mode="svg"
    )


st.plotly_chart(
    fig_area_price,
    use_container_width=True,
    key="area_price_chart"
)


# --------------------------------------------------
# BHK PIE CHART
# --------------------------------------------------

st.header(
    "BHK Pie Chart"
)

sector_options = (
    new_df[
        "sector"
    ]
    .unique()
    .tolist()
)

sector_options.insert(
    0,
    "Overall"
)


selected_sector_pie = st.selectbox(
    "Select Sector",
    sector_options,
    key="sector_pie_select"
)


if selected_sector_pie == "Overall":

    fig_pie = px.pie(
        new_df,
        names="bedRoom",
        title=(
            "BHK Distribution "
            "for All Sectors"
        )
    )

else:

    fig_pie = px.pie(

        new_df[
            new_df["sector"]
            == selected_sector_pie
        ],

        names="bedRoom",

        title=(
            f"BHK Distribution in "
            f"{selected_sector_pie}"
        )
    )


st.plotly_chart(
    fig_pie,
    use_container_width=True,
    key="bhk_pie_chart"
)


# --------------------------------------------------
# BHK PRICE COMPARISON
# --------------------------------------------------

st.header(
    "Side by Side BHK Price Comparison"
)


selected_sector_box = st.selectbox(
    "Select Sector for Price Comparison",
    sector_options,
    key="sector_box_select"
)


if selected_sector_box == "Overall":

    box_df = new_df[
        new_df["bedRoom"] <= 4
    ]

    title_suffix = "All Sectors"

else:

    box_df = new_df[
        (
            new_df["sector"]
            == selected_sector_box
        )
        &
        (
            new_df["bedRoom"] <= 4
        )
    ]

    title_suffix = (
        selected_sector_box
    )


fig_box = px.box(

    box_df,

    x="bedRoom",

    y="price",

    title=(
        f"BHK Price Range for "
        f"{title_suffix}"
    )
)


st.plotly_chart(
    fig_box,
    use_container_width=True,
    key="bhk_price_box_chart"
)


# --------------------------------------------------
# PRICE DISTRIBUTION
# --------------------------------------------------

st.header(
    "Side by Side Distplot for Property Type"
)


fig_dist = plt.figure(
    figsize=(10, 4)
)


sns.distplot(

    new_df[
        new_df["property_type"]
        == "house"
    ]["price"],

    label="House"
)


sns.distplot(

    new_df[
        new_df["property_type"]
        == "flat"
    ]["price"],

    label="Flat"
)


plt.legend()


st.pyplot(
    fig_dist,
    use_container_width=True
)