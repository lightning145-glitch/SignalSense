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
        conn.execute(
            "INSERT INTO opportunities (org_id, title, description, skills_required, location_text) VALUES (?,?,?,?,?)",
            (1, row["tittle"], row["description"], row["skills"], row.get("location", ""))
        )
        conn.commit()
        conn.close()
        print("Dataset loaded.")
        
if __name__ == "__main__":
    load_kaggle_data("D:\VS\SignalSense\Volunteer-match.csv")