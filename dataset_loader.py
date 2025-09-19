import sqlite3
import pandas as pd

DB = "database.db"

def load_kaggle_data(csv_path):
    df = pd.read_csv(csv_path)

    df["text"] = (
        df["title"].fillna("") + " " + df["description"].fillna("") + " " + df["skills"].fillna("")
    )

    conn = sqlite3.connect(DB)
    
    for _, row in df.iterrows():
        location = row.get("location", "")

        conn.execute(
            """
            INSERT INTO opportunities (org_id, title, description, skills_required, location_text)
            VALUES (?, ?, ?, ?, ?)
            """,
            (1, row["title"], row["description"], row["skills"], location)
        )
    
    conn.commit()
    conn.close()
    print("Dataset loaded successfully.")

if __name__ == "_main_":
    csv_file = "D:\VS\SignalSense\Volunteer-match.csv"  
    load_kaggle_data(csv_file)