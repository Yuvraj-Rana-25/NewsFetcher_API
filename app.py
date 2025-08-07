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
       /* Set default cursor to arrow for everything */
        * {
            cursor: default !important;
        }

        /* Ensure entire button (including text) shows pointer */
        button, button * {
            cursor: pointer !important;
        }

        /* Ensure links styled as "Read Full Article" also show pointer */
        a, a * {
            cursor: pointer !important;
        }

        /* Search bar text input gets text (I-beam) cursor */
        input[type="text"] {
            cursor: text !important;
        }
    </style>
""", unsafe_allow_html=True)


# Ensure session state has key
if "active_category" not in st.session_state:
    st.session_state["active_category"] = None


# Search box
st.markdown("## 🔍 Search for Live News")


with st.form("search_form", clear_on_submit=True):
    topic = st.text_input("Enter a topic to fetch related news", value="", key="topic_input")
    st.markdown("""
        <script>
        document.addEventListener('DOMContentLoaded', function () {
            const inputBox = document.querySelector('input[type="text"]');
            
            // Blur on scroll
            window.addEventListener('scroll', () => {
                if (inputBox === document.activeElement) {
                    inputBox.blur();
                }
            });

            // Blur when clicking outside the input
            document.addEventListener('click', function (event) {
                if (inputBox && !inputBox.contains(event.target)) {
                    inputBox.blur();
                }
            });

            // Blur on enter key press
            if (inputBox) {
                inputBox.addEventListener('keydown', function (e) {
                    if (e.key === "Enter") {
                        inputBox.blur();
                    }
                });
            }
        });
        </script>
    """, unsafe_allow_html=True)
    submitted = st.form_submit_button("Fetch News")

if submitted and topic:
    with st.spinner("Fetching news..."):
        headlines = fetch_headlines(topic)
        save_to_json(headlines)
        save_to_db(headlines, topic)
        st.success("News fetched and stored successfully!")

        # Show the fetched headlines immediately
        if headlines:
            st.markdown(f"### 🗞️ Latest headlines about **{topic.capitalize()}**:")
            for article in headlines[:10]:
                st.markdown(f"**{article.get('title')}**")
                st.markdown(f"[Read full article]({article.get('link')})", unsafe_allow_html=True)
                st.markdown("---")




# Browse by category



# Sidebar Categories
st.sidebar.markdown("### 🗂️ Categories")
CATEGORIES = [cat for cat in CATEGORY_KEYWORDS.keys() if cat.lower() != "top"]

# Show all buttons in sidebar as rows
for category in CATEGORIES:
    if st.sidebar.button(category.capitalize()):
        # If the same category is clicked again, deselect it
        if st.session_state.get("active_category") == category:
            st.session_state["active_category"] = None
        else:
            st.session_state["active_category"] = category
            category_headlines = get_category_view(category)
            if not category_headlines.empty:
                st.markdown(f"### 🗞️ Latest headlines about **{category.capitalize()}**:")
                for index, row in category_headlines.iterrows():
                    st.subheader(row["title"])
                    st.markdown(f"**Source:** {row['source']}  \n📅 *{row['publishedAt']}*")
                    st.markdown(f"[Read full article]({row['url']})", unsafe_allow_html=True)
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

st.markdown("<center><small>Crafted with ❤️ by Yuvraj Rana · Powered by NewsData.io API</small></center>", unsafe_allow_html=True)
