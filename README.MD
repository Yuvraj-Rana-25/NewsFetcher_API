# 📰 News Headline Fetcher (using NewsData.io API)

This Python project fetches and stores the latest news headlines based on a user-specified topic. It uses the NewsData.io API and demonstrates key practices in API integration, modular Python scripting, file handling, and secure key management.

---

## 📁 Project Structure

- `main.py`: Core Python script that handles the API request, data processing, and saving headlines.
- `headlines.json`: Output file that stores all fetched headlines in structured JSON format.
- `.env`: Stores the API key securely (excluded from version control).
- `.gitignore`: Prevents sensitive files like `.env` from being committed to Git.
- `README.md`: Documentation for the project and learning summary.

---

## 🧠 What I Learned

### ✅ Environment Setup & Git
- Connected VS Code with GitHub to manage version control directly.
- Created a new repository specifically for this project.
- Used a `.gitignore` file to exclude sensitive files like `.env`.

### ✅ API Key Handling
- Stored the API key securely in a `.env` file.
- Loaded it into the script using `python-dotenv` and `os.getenv()` to avoid hardcoding secrets.

### ✅ Script Logic
- Imported necessary modules: `os`, `requests`, `json`, and `dotenv`.
- Defined two modular functions:
  - `fetch_headlines(topic, language, country)`: Makes a GET request to NewsData API and parses the JSON response.
  - `save_to_json(headlines)`: Saves the list of fetched articles to a local `.json` file in UTF-8 encoding.
- Used basic error handling to check if the API call was successful (`status_code == 200`).
- Used `if __name__ == "__main__"` to ensure the script only runs when executed directly.
- Prompted the user for a topic, fetched relevant headlines, and displayed the top 5 results.

---

## 🚀 Technologies Used

- Python 3
- [NewsData.io API](https://newsdata.io/)
- `requests` – to make API calls
- `json` – for handling structured data
- `dotenv` – for environment variable management
- VS Code + Git + GitHub – for code editing and version control

---

## 📌 Next Steps / Ideas to Expand
- Add keyword-based filtering within the fetched headlines.
- Let user choose between saving `.json` or `.txt` format.
- Create a Streamlit dashboard to display news interactively.
- Filter by country or language dynamically via user input.

---

## 🙌 Personal Note

This project helped me go beyond tutorials — I now understand how real-world APIs interact with Python scripts, how to handle data safely and modularly, and how to manage code cleanly through Git and GitHub. It's my first structured step toward becoming a data product builder.

