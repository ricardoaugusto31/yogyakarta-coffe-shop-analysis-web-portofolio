import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse
import requests

# =====================================================================
# 1. PAGE CONFIGURATION & STYLING
# =====================================================================
# Set the page configuration for the Streamlit app.
st.set_page_config(
    page_title="Yogya Coffee Compass",
    page_icon="🧭",
    layout="wide"
)

# Inject custom CSS for styling UI elements.
st.markdown("""
<style>
    /* Style for the metric cards */
    div[data-testid="stMetric"] {
        background-color: #2E2E2E; /* Secondary background color */
        border: 1px solid #2E2E2E;
        border-radius: 10px;
        padding: 15px;
        color: #D3A26A; /* Primary text color */
    }

    /* Style for the labels within the metric cards */
    div[data-testid="stMetricLabel"] {
        color: #FFFFFF; /* Secondary text color */
    }
    
    /* Style for hyperlinks to match the primary theme color */
    a:link, a:visited {
        color: #D3A26A;
        text-decoration: none; /* Remove the default underline */
    }

    a:hover, a:active {
        text-decoration: underline; /* Add underline on hover for user feedback */
        color: #E6B88A; /* Slightly lighter color on hover */
    }
</style>
""", unsafe_allow_html=True)


# =====================================================================
# 2. HELPER FUNCTIONS
# =====================================================================
@st.cache_data
def load_and_process_data():
    """
    Loads the final scored coffee shop data, cleans the display names,
    and classifies each shop into its respective segment.
    This function is cached to improve performance.
    """
    df = pd.read_csv('data/coffee_shop_scores_final.csv')
    
    # Clean the 'OrganizationName' field for better readability.
    def clean_display_name(name):
        if isinstance(name, str):
            if 'Alamat: ' in name: name = name.replace('Alamat: ', '')
            return name.split(',')[0].strip() # Use the first part of the address
        return 'Unknown Name'
    df['DisplayName'] = df['OrganizationName'].apply(clean_display_name)
    
    # Classify shops into segments based on the median scores.
    median_nugas = df['Nugas_Score_Normalized'].median()
    median_nongkrong = df['Nongkrong_Score_Normalized'].median()
    def assign_segment(row):
        is_nugas_high = row['Nugas_Score_Normalized'] >= median_nugas
        is_nongkrong_high = row['Nongkrong_Score_Normalized'] >= median_nongkrong
        if is_nugas_high and is_nongkrong_high: return 'All-Rounder'
        elif is_nugas_high: return 'Productivity Hub'
        elif is_nongkrong_high: return 'Social Hotspot'
        else: return 'General Purpose'
    df['Segment'] = df.apply(assign_segment, axis=1)
    return df

@st.cache_data
def get_github_avatar(username):
    """
    Fetches a user's avatar URL from the GitHub API.
    Includes a fallback URL in case the API call fails.
    """
    url = f"https://api.github.com/users/{username}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json().get("avatar_url")
    except requests.RequestException:
        # Fallback in case of API failure or invalid username
        return "https://avatars.githubusercontent.com/u/9919?s=400"

# Load the data into the app
df_scores = load_and_process_data()


# =====================================================================
# 3. MAIN TITLE & HEADER
# =====================================================================
st.title('🧭 Yogya Coffee Compass')
st.markdown("Your smart guide to finding the best coffee shops in Yogyakarta for **working** or **socializing**.")
st.markdown("---")


# =====================================================================
# 4. SIDEBAR WITH FILTERS AND BRANDING
# =====================================================================
st.sidebar.header('🔍 Filter Your Preferences')

# Define persona options for the selectbox
persona_map = {
    'I want to work/study 🧑‍💻': 'Productivity Hub',
    'I want to socialize 🤳': 'Social Hotspot',
    'I want the best of both 🌟': 'All-Rounder'
}
persona_choice_label = st.sidebar.selectbox('Select your main need:', list(persona_map.keys()))
selected_segment = persona_map[persona_choice_label]

# Define interactive filters
min_rating = st.sidebar.slider('Minimum Star Rating:', 4.0, 5.0, 4.5, 0.1)
min_reviews = st.sidebar.slider('Minimum Number of Reviews:', 0, 1000, 50, 10)

# Personal branding and project links
st.sidebar.markdown("---")
st.sidebar.header("About This Project")
st.sidebar.info(
    "This application is the final product of an in-depth data analysis project. "
    "[The data was processed from thousands of Google Maps reviews to provide objective recommendations](https://github.com/ricardoaugusto31/yogyakarta-coffee-shop-analysis)."
)
st.sidebar.header("Created by")
github_username = "ricardoaugusto31"
avatar_url = get_github_avatar(github_username)
st.sidebar.image(avatar_url, width=100)
st.sidebar.markdown(
    f"""
    **Ricardo Augusto**
    
    [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/ricardo-yan-augusto-003516308/) 
    [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/{github_username})
    """
)


# =====================================================================
# 5. MAIN PAGE LOGIC AND DISPLAY
# =====================================================================
# Apply filters to the dataframe
filtered_df = df_scores[
    (df_scores['Segment'] == selected_segment) &
    (df_scores['RateStars'] >= min_rating) &
    (df_scores['ReviewsTotalCount'] >= min_reviews)
].sort_values(by='RateStars', ascending=False)

# Display the header for the recommendations
st.header(f"✨ Top Recommendations for: {persona_choice_label}")
st.write(f"Displaying **{len(filtered_df)}** coffee shops that match your criteria.")

if filtered_df.empty:
    st.warning("No coffee shops match your current filters. Try adjusting the criteria.")
else:
    # --- Interactive Map Display ---
    st.subheader("Location Map")
    map_center = [-7.7956, 110.3695] # Central point of Yogyakarta
    m = folium.Map(location=map_center, zoom_start=13)

    for idx, row in filtered_df.iterrows():
        if pd.notna(row['OrganizationLatitude']) and pd.notna(row['OrganizationLongitude']):
            popup_html = f"<b>{row['DisplayName']}</b><br>Rating: {row['RateStars']} ⭐"
            folium.Marker(
                [row['OrganizationLatitude'], row['OrganizationLongitude']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=row['DisplayName']
            ).add_to(m)
    st_folium(m, width='100%', height=400)

    # --- Detailed List of Recommendations ---
    st.subheader("Detailed List")
    # Display the top 10 results from the filtered dataframe
    for i, (idx, row) in enumerate(filtered_df.head(10).iterrows(), 1):
        
        # Create a safe URL for Google Maps search
        query = urllib.parse.quote_plus(f"{row['DisplayName']} Yogyakarta")
        maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"
        
        # Display the name as a clickable hyperlink
        st.markdown(f"#### #{i} [{row['DisplayName']}]({maps_url})")

        # Display key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="⭐ Rating", value=f"{row['RateStars']:.1f} / 5.0")
        with col2:
            st.metric(label="💬 Review Count", value=int(row['ReviewsTotalCount']))
        with col3:
            st.metric(label="🧑‍💻 Productivity Score", value=f"{row['Nugas_Score_Normalized']:.2f}")
        with col4:
            st.metric(label="🤳 Social Score", value=f"{row['Nongkrong_Score_Normalized']:.2f}")
        st.markdown("---")
