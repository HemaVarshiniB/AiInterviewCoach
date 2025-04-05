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
            user_response TEXT,
            question_category TEXT,
            question_score REAL,
            question_feedback TEXT,
            FOREIGN KEY (round_id) REFERENCES interview_rounds(round_id)
        )
    """)

    # Add 'user_response' column to interview_questions if it doesn't exist
    # cursor.execute("PRAGMA table_info(interview_questions)")
    # columns = [column[1] for column in cursor.fetchall()]
    # if "user_response" not in columns:
    #     cursor.execute("ALTER TABLE interview_questions ADD COLUMN user_response TEXT")

    conn.commit()
    conn.close()
    print("Tracking tables created and sample data inserted successfully.")

# Run the function
init_interview_tracking_db()
