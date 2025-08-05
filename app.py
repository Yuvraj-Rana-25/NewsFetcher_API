import streamlit as st
from main import fetch_headlines, save_to_json
from db import save_to_db, get_recent_headlines
from views import get_category_view, CATEGORY_KEYWORDS

# Page config
st.set_page_config(page_title="NewsPulse - Real-time News", page_icon="📰", layout="wide")

# Inject CSS styling
st.markdown("""
    <style>
        .reportview-container .main .block-container {
            padding-top: 2rem;
            padding-right: 3rem;
            padding-left: 3rem;
            padding-bottom: 2rem;
        }

        .stTextInput > div > div > input {
            background-color: #1e1e1e;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 10px;
        }

        .stButton>button {
            color: white;
            background-color: #0066cc;
            border-radius: 8px;
            padding: 0.5em 1em;
            font-weight: bold;
        }

        .stButton>button:hover {
            background-color: #0052a3;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Search box
st.markdown("## 🔍 Search for Live News")
topic = st.text_input("Enter a topic to search:", placeholder="e.g. elections, Apple, cricket...")

if st.button("🔎 Fetch Live News"):
    if topic:
        with st.spinner("Fetching latest headlines..."):
            headlines = fetch_headlines(topic)
            if headlines:
                save_to_json(headlines)
                save_to_db(headlines, topic)
                st.success("✅ Headlines fetched and saved successfully!")
            else:
                st.warning("⚠️ No headlines found for that topic.")
    else:
        st.warning("❗ Please enter a topic to search.")



# Browse by category

st.markdown("### 📂 Browse Top News by Category")

# Dropdown selector for category
selected_category = st.selectbox(
    "Select a news category",
    options=list(CATEGORY_KEYWORDS.keys()),
    index=0  # Default to "top" category
)

# Show news for selected category
df = get_category_view(selected_category)

if df.empty:
    st.warning("No news available for this category.")
else:
    st.success(f"Top {selected_category.capitalize()} Headlines:")
    for _, row in df.iterrows():
        st.subheader(row["title"])
        st.markdown(f"**Source:** {row['source']}  \n📅 *{row['publishedAt']}*")
        st.markdown(f"[Read full article]({row['url']})", unsafe_allow_html=True)
        st.markdown("---")





st.markdown("---")



# Recently fetched headlines
st.markdown("### 🕘 Recently Fetched Headlines")
headlines = get_recent_headlines(limit=5)
if headlines:
    for article in headlines:
        st.subheader(article["title"])
        st.markdown(f"**Source:** {article['source']}  \n📅 *{article['publishedAt']}*")
        st.markdown(f"[Read full article]({article['url']})", unsafe_allow_html=True)
        st.markdown("---")
else:
    st.warning("No recent headlines fetched yet. Try searching above!")


# Footer
st.markdown("---")
st.markdown("<center><small>Crafted with ❤️ by Yuvraj Rana · Powered by NewsData.io API</small></center>", unsafe_allow_html=True)
