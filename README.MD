# 📰 NewsPulse — Live + Stored News Fetcher App

**NewsPulse** is a modular Python application that fetches real-time news using the NewsData.io API, stores the data in a MySQL database, and displays both live and stored headlines in a clean, interactive Streamlit web interface.

This project serves as a foundational step toward building full-stack data-driven applications with end-to-end functionality — from API integration to GUI-based output.

---

## 🚀 Features

- 🔍 Fetch live news headlines by topic
- 💾 Save results in a MySQL database
- 📂 Store offline JSON backups (optional)
- 🧠 Retrieve and display recent news from database
- 🖥️ Interactive GUI using Streamlit
- 🔒 Secure API keys with dotenv
- 📌 Full Git-based version control

---

## 🛠️ Technologies Used

| Layer          | Tools/Technologies         |
|----------------|----------------------------|
| **Frontend**   | Streamlit                  |
| **Backend**    | Python, requests, dotenv   |
| **Database**   | MySQL                      |
| **Versioning** | Git & GitHub               |

---


## 📁 Project Structure



news_fetcher_api/  
├── app.py            ← Streamlit GUI app  
├── main.py           ← Fetch & process live news from API  
├── db.py             ← Save/retrieve news from MySQL database  
├── headlines.json    ← Optional JSON backup of fetched news  
├── .env              ← API key (excluded from Git)  
├── .gitignore        ← Ignore .env, __pycache__, *.pyc, etc.  
└── README.md         ← This file  




---

## ⚙️ How It Works

### 🧩 Modular Components

1. `main.py`
   - Contains `fetch_headlines()` to call NewsData.io API
   - Includes `save_to_json()` to optionally back up data offline
   - Protected with `if __name__ == "__main__"` for safe testing

2. `db.py`
   - Contains `save_to_db()` to write fetched news into MySQL
   - Contains `get_recent_headlines()` to read from DB by topic

3. `app.py`
   - Streamlit GUI
   - Text input for news topic
   - "Fetch Live News" button → fetch + save new data
   - Displays latest headlines from MySQL database

---

## 💡 Current Behavior & UX Notes

- ✅ GUI allows entering a topic and fetching news manually
- ❌ **Pressing Enter** in the topic field **only updates stored results**, not live API fetch
- 🧠 This avoids excessive API calls during development/testing
- 📌 **TODO**: Combine Enter key and fetch button behavior using Streamlit Forms

---


## 🧪 How to Run & Test

- **Run the GUI app**: `streamlit run app.py`
- **Run the API logic for testing**: `python main.py`
- **Run the database module to verify DB connection**: `python db.py`



## ⚠️ Known Limitations

🔌 Manual button click required for fetching new news

🌐 API quota is limited per day (free tier)

🔐 API key stored in .env file (excluded from Git)


## 🗺️ Future Improvements

✅ Add streamlit form to unify Enter and button triggers

✅ Add category-based filtering or keyword dropdown

✅ Improve DB schema for multiple categories, timestamps, etc.

✅ Export results to CSV/PDF

✅ Deploy on Streamlit Cloud or HuggingFace Spaces

✅ Add user analytics or session tracking


