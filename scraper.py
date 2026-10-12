import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "tech_jobs.db"


def init_db():
    """Create the database and jobs table if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            skills TEXT,
            location TEXT,
            date_added TEXT
        )
    """)
    conn.commit()
    conn.close()


def fetch_and_store_jobs(n_rows=200):
    """Generate mock job listings (stand-in for a real scraper's output)."""
    titles = ["Data Analyst", "Software Engineer", "Python Developer",
              "QA Engineer", "Business Analyst", "Cloud Engineer"]
    skills_pool = [
        ["Python", "SQL", "Excel"],
        ["Java", "Spring Boot", "SQL"],
        ["Python", "Pandas", "Streamlit"],
        ["Selenium", "Java", "Testing"],
        ["SQL", "Tableau", "Excel"],
        ["Python", "AWS", "Docker"],
    ]
    companies = ["TCS", "Infosys", "Wipro", "Cognizant", "Tech Startup X", "Accenture"]
    locations = ["Bangalore", "Hyderabad", "Mumbai", "Remote", "Pune", "Chennai"]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Mock data only: wipe old rows so re-running doesn't create duplicates.
    cursor.execute("DELETE FROM jobs")

    for _ in range(n_rows):
        idx = random.randint(0, len(titles) - 1)
        date_added = (datetime.today() - timedelta(days=random.randint(0, 29))).strftime("%Y-%m-%d")
        cursor.execute(
            """INSERT INTO jobs (title, company, skills, location, date_added)
               VALUES (?, ?, ?, ?, ?)""",
            (titles[idx], random.choice(companies), ", ".join(skills_pool[idx]),
             random.choice(locations), date_added),
        )

    conn.commit()
    conn.close()
    print(f"Successfully stored {n_rows} job listings in {DB_NAME}")


if __name__ == "__main__":
    init_db()
    fetch_and_store_jobs()