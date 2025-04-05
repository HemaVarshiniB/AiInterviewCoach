import sqlite3
from datetime import datetime

def init_interview_tracking_db():
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    # Create interview_sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            company_name TEXT,
            role TEXT,
            experience TEXT,
            interview_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            session_performance INTEGER
        )
    """)

    # Create interview_rounds table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS round_performance (
            round_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            user_id INTEGER NOT NULL,
            round_type TEXT,
            round_score REAL,
            round_feedback TEXT,
            FOREIGN KEY (session_id) REFERENCES interview_sessions(session_id)
        )
    """)

    # Create interview_questions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_questions (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            round_id INTEGER,
            question_text TEXT,
            question_category TEXT,
            question_score REAL,
            question_feedback TEXT,
            FOREIGN KEY (round_id) REFERENCES interview_rounds(round_id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tracking tables created and sample data inserted successfully.")

# Run the function
init_interview_tracking_db()
