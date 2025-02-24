import streamlit as st
import requests
import pandas as pd

# ---- UI DESIGN ----
st.set_page_config(page_title="Instagram Trend Analysis", layout="wide")
st.title("📊 Real-Time Instagram Trend Analysis")

# Sidebar Inputs
st.sidebar.header("Filter Trends")
hashtag = st.sidebar.text_input("Enter Hashtag (without #)", "technology")
num_posts = st.sidebar.slider("Number of Posts", 10, 100, 50)

# ---- BACKEND (Fetch Instagram Data) ----
INSTAGRAM_API_URL = f"https://www.instagram.com/explore/tags/{hashtag}/?__a=1"

@st.cache_data  # Cache to avoid multiple API calls
def fetch_instagram_data():
    try:
        response = requests.get(INSTAGRAM_API_URL)
        if response.status_code == 200:
            data = response.json()
            posts = data['graphql']['hashtag']['edge_hashtag_to_media']['edges']
            return posts
    except Exception as e:
        st.error(f"Error fetching data: {e}")
    return []

posts = fetch_instagram_data()

# ---- DISPLAY DATA ----
if posts:
    df = pd.DataFrame([
        {"Username": post['node']['owner']['username'], 
         "Likes": post['node']['edge_liked_by']['count'],
         "Comments": post['node']['edge_media_to_comment']['count'],
         "Caption": post['node']['edge_media_to_caption']['edges'][0]['node']['text'] if post['node']['edge_media_to_caption']['edges'] else ""}
        for post in posts[:num_posts]
    ])
    
    st.dataframe(df)

    # ---- Charts ----
    st.subheader("📈 Engagement Metrics")
    st.bar_chart(df.set_index("Username")[["Likes", "Comments"]])
else:
    st.warning("No data found. Try another hashtag.")
