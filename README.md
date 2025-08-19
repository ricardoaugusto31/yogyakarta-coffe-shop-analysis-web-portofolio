# Yogya Coffee Compass: An Interactive Web App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://yogyacoffecompas.streamlit.app/)

This repository contains the source code for the "Yogya Coffee Compass," an interactive Streamlit web application that serves as the portfolio front-end for the [Yogyakarta Coffee Shop Analysis project](https://github.com/ricardoaugusto31/yogyakarta-coffee-shop-analysis).

The purpose of this app is to present the analytical findings in an engaging, user-friendly, and interactive format.

---

### 🖼️ Application Preview

<img width="1919" height="907" alt="image" src="https://github.com/user-attachments/assets/a098c4e9-2d3b-489d-8c2a-890870997786" />

<img width="1918" height="923" alt="image" src="https://github.com/user-attachments/assets/15bed902-07fa-4add-9b8b-4ef9da7cd55b" />

---

### ✨ Key Features

This web application allows users to:
* **Filter by Persona:** Dynamically find coffee shops best suited for working/studying, socializing, or a mix of both.
* **Adjust Criteria:** Use interactive sliders to filter recommendations by minimum star rating and review count.
* **Explore on a Map:** View the locations of all recommended coffee shops on an interactive map powered by Folium.
* **Get Detailed Recommendations:** See a ranked list of the top 10 coffee shops that match the selected criteria, complete with key metrics.
* **Direct Google Maps Link:** Click on any recommended coffee shop's name to instantly search for it on Google Maps.

### 🛠️ Tech Stack

The application is built entirely in Python using the following libraries:
* **Web Framework:** [Streamlit](https://streamlit.io/)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
* **Interactive Maps:** [Folium](https://python-visualization.github.io/folium/) & `streamlit-folium`
* **API Interaction:** [Requests](https://requests.readthedocs.io/en/latest/) (for fetching GitHub avatar)

### 🔗 Relationship to the Analysis Project

This web application is the final product of a comprehensive data analysis project.

* **The "How" (The Analysis):** The complete end-to-end analysis, including data cleaning, advanced NLP, and the scoring model, can be found in the [**analysis repository**](https://github.com/ricardoaugusto31/yogyakarta-coffee-shop-analysis).
* **The "What" (This App):** This repository takes the final, processed dataset from that analysis (`coffee_shop_scores_final.csv`) and builds an interactive user interface on top of it.

This separation demonstrates a complete project lifecycle, from raw data processing to a polished, user-facing product.

### 🚀 How to Run Locally

1.  **Clone this repository:**
    ```bash
    git clone [https://github.com/ricardoaugusto31/yogyakarta-coffe-shop-analysis-web-portofolio.git](https://github.com/ricardoaugusto31/yogyakarta-coffe-shop-analysis-web-portofolio.git)
    cd yogyakarta-coffe-shop-analysis-web-portofolio
    ```
2.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    The application will open in a new tab in your web browser.
