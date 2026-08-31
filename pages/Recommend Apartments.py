import streamlit as st
import pandas as pd
import pickle
from sklearn.metrics.pairwise import euclidean_distances


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Recommend Apartments",
    layout="wide"
)


# --------------------------------------------------
# LOAD LOCATION DATA
# --------------------------------------------------

with open("data/location_distance.pkl", "rb") as f:
    location_df = pickle.load(f)


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("Select Location and Radius")


# --------------------------------------------------
# LOCATION AND RADIUS INPUT
# --------------------------------------------------

selected_location = st.selectbox(
    "Location",
    sorted(location_df.columns.tolist())
)

radius = st.number_input(
    "Radius in Kms",
    min_value=0.0,
    value=5.0,
    step=1.0
)


# --------------------------------------------------
# SEARCH APARTMENTS
# --------------------------------------------------

if st.button("Search", key="search_button"):

    result_ser = (
        location_df[
            location_df[selected_location] <= radius * 1000
        ][selected_location]
        .sort_values()
    )

    st.session_state["search_results"] = result_ser
    st.session_state["selected_location"] = selected_location


# --------------------------------------------------
# DISPLAY SEARCH RESULTS
# --------------------------------------------------

if (
    "search_results" in st.session_state
    and not st.session_state["search_results"].empty
):

    result_ser = st.session_state["search_results"]

    st.markdown(
        f"### Apartments near "
        f"{st.session_state['selected_location']}"
    )

    for key, value in result_ser.items():

        st.text(
            f"{key}   "
            f"{round(value / 1000, 2)} kms"
        )


    # --------------------------------------------------
    # SIMILAR APARTMENTS
    # --------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### Find Similar Apartments"
    )

    selected_apartment = st.selectbox(
        "Select an apartment from the results to find similar ones:",
        result_ser.index.tolist(),
        key="apartment_select"
    )


    if st.button(
        "Find Similar",
        key="find_similar_button"
    ):

        # Get selected apartment's location vector
        selected_vector = location_df.loc[
            [selected_apartment]
        ]


        # Calculate Euclidean distances
        distances = euclidean_distances(
            selected_vector,
            location_df
        )[0]


        # Create distance series
        dist_series = pd.Series(
            distances,
            index=location_df.index
        )


        # Get top 5 similar apartments
        # Exclude the selected apartment itself
        top_similar = (
            dist_series
            .sort_values(ascending=True)
            .iloc[1:6]
        )


        st.markdown(
            f"**Apartments geographically closest to "
            f"{selected_apartment}:**"
        )


        for apt_name, dist_score in top_similar.items():

            dist_to_loc = location_df.loc[
                apt_name,
                st.session_state["selected_location"]
            ]

            st.text(
                f"{apt_name}   "
                f"{round(dist_to_loc / 1000, 2)} kms "
                f"from "
                f"{st.session_state['selected_location']}"
            )


# --------------------------------------------------
# NO RESULTS MESSAGE
# --------------------------------------------------

elif (
    "search_results" in st.session_state
    and st.session_state["search_results"].empty
):

    st.warning(
        "No apartments found within the selected radius."
    )