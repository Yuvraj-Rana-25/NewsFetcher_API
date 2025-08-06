import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
# here we load environment variables from a .env file
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
# here we create the headlines table
def create_headlines_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS headlines (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title TEXT,
            description TEXT,
            source VARCHAR(255),
            publishedAt DATETIME,
            url TEXT,
            topic VARCHAR(255)
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_headlines_table()
    print(" headlines table is ready.")

# here we save the headlines to the database
def save_to_db(headlines, topic):
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO headlines (title, description, source, publishedAt, url, topic, category)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    check_query = "SELECT COUNT(*) FROM headlines WHERE url = %s"

    for article in headlines:
        try:
            title = article.get('title')
            description = article.get('description')
            source = article.get('source')
            publishedAt = article.get('pubDate')
            url = article.get('link')
            category = article.get('category', 'general')  # fallback

            if isinstance(source, list):
                source = ", ".join(source)

            if isinstance(category, list):
                category = ", ".join(category)          
            if not title or not url:
                continue

            # ✅ Check for duplicate
            cursor.execute(check_query, (url,))
            count = cursor.fetchone()[0]
            if count > 0:
                continue  # Skip inserting if already exists

            cursor.execute(insert_query, (title, description, source, publishedAt, url, topic, category))

        except Exception as e:
            print("❌ Error inserting article:", e)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Data saved to MySQL successfully.")


# here we fetch recent headlines from the database about mentioned topic
def get_recent_headlines(limit=5, topic=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if topic:
        cursor.execute("""
            SELECT * FROM headlines
            WHERE topic = %s
            ORDER BY publishedAt DESC
            LIMIT %s
        """, (topic, limit))
    else:
        cursor.execute("""
            SELECT * FROM headlines
            ORDER BY publishedAt DESC
            LIMIT %s
        """, (limit,))

    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
