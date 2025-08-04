import streamlit as st
from db import get_recent_headlines, save_to_db
from main import fetch_headlines

st.set_page_config(page_title="NewsPulse", layout="wide")
st.title("🗞️ NewsPulse")

# --- INPUT ---
topic = st.text_input("Enter a topic to fetch news:", "")

# --- FETCH BUTTON ---
if st.button("📥 Fetch Latest News"):
    if topic.strip():
        with st.spinner("Fetching news..."):
            try:
                headlines = fetch_headlines(topic=topic)
                save_to_db(headlines, topic)
                st.success(f"✅ {len(headlines)} headlines fetched and stored.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a topic first.")

# --- SHOW STORED HEADLINES ---
st.subheader("📰 Stored Headlines")
stored = get_recent_headlines(topic=topic if topic else None, limit=5)

if stored:
    for i, article in enumerate(stored, start=1):
        st.markdown(f"### {i}. [{article['title']}]({article['url']})")
        st.caption(f"{article['source']} | {article['publishedAt']}")
        st.write(article['description'])
        st.markdown("---")
else:
    st.info("No stored headlines found.")
