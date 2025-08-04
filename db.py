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
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO headlines (title, description, source, publishedAt, url, topic)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    for article in headlines:
        try:
            title = article.get('title')
            description = article.get('description')
            source = article.get('source_id')  # adjust if key is different in future api structure
            publishedAt = article.get('pubDate')  # ISO string format
            url = article.get('link')

            # Check for missing fields or bad data
            if not title or not url:
                continue

            cursor.execute(insert_query, (title, description, source, publishedAt, url, topic))

        except Exception as e:
            print(" Error inserting article:", e)

    conn.commit()
    cursor.close()
    conn.close()
    print(" Headlines inserted into database.")

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
