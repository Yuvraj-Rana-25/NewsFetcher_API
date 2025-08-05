import pymysql
import pandas as pd

# ✅ Define all news categories 
CATEGORY_KEYWORDS = {
    "entertainment": ["movie", "film", "music", "actor", "celebrity", "award"],
    "sports": ["cricket", "football", "tournament", "match", "olympic", "goal"],
    "politics": ["election", "government", "parliament", "minister", "bjp", "congress"],
    "economy": ["gdp", "inflation", "stock", "market", "trade", "finance"],
    "technology": ["ai", "tech", "robot", "software", "gadget", "app", "startup"],
    "science": ["research", "nasa", "space", "physics", "scientist"],
    "health": ["covid", "health", "vaccine", "disease", "hospital", "doctor"],
    "world": ["usa", "china", "global", "international", "war", "un"],
    "top": []  # special view: raw top news
}

# ✅ Function to create or update views for each category
def create_views():
    print("📡 Connecting to MySQL...")

    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='yuvisql2010',  
            database='newspulse',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as conn_error:
        print("❌ Failed to connect to database:", conn_error)
        return

    print("✅ Connected to MySQL.")

    try:
        with connection.cursor() as cursor:
            for category, keywords in CATEGORY_KEYWORDS.items():
                view_name = f"view_{category.lower()}"
                
                # Always include the category label from API
                conditions = [f"category = %s"]
                params = [category]

                # Add keyword-based matching for broader coverage
                for kw in keywords:
                    conditions.append("title LIKE %s")
                    conditions.append("description LIKE %s")
                    params.append(f"%{kw}%")
                    params.append(f"%{kw}%")

                where_clause = " OR ".join(conditions)

                query = f"""
                CREATE OR REPLACE VIEW `{view_name}` AS
                SELECT * FROM headlines
                WHERE {where_clause}
                ORDER BY publishedAt DESC
                LIMIT 10;
                """

                try:
                    cursor.execute(query, params)
                    print(f"✅ Created/Updated view: {view_name}")
                except Exception as e:
                    print(f"❌ Failed to create view {view_name}: {e}")

        connection.commit()

    except Exception as overall_error:
        print("❌ Unexpected error during view creation:", overall_error)

    finally:
        connection.close()
        print("🔌 MySQL connection closed.")


# ✅ Function to fetch headlines from a given view as a DataFrame
def get_category_view(category):
    """
    Fetch top 10 headlines from the view corresponding to the category.
    Returns a pandas DataFrame.
    """
    view_name = f"view_{category.lower()}"

    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='yuvisql2010',  
            database='newspulse',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `{view_name}`;")
            results = cursor.fetchall()
            return pd.DataFrame(results)

    except Exception as e:
        print(f"❌ Error fetching from {view_name}:", e)
        return pd.DataFrame()

    finally:
        connection.close()


# ✅ Main block to trigger view creation from CLI
if __name__ == "__main__":
    print("🚀 Running views.py")
    print("📂 Loaded categories:", CATEGORY_KEYWORDS.keys)
    create_views()
