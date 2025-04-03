import sqlite3

def init_db():
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_stages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            experience_level TEXT,
            role TEXT,
            num_rounds INTEGER,
            round_details TEXT
        )
    """)

    # Sample Data
    sample_data = [
        ("Google", "Fresher", "Software Engineer", 3, "Coding, System Design, Behavioral"),
        ("Google", "Mid-Level", "Software Engineer", 4, "Coding, System Design, System Thinking, Behavioral"),
        ("Meta", "Fresher", "Data Scientist", 3, "Coding, ML Concepts, Behavioral"),
        ("Meta", "Senior", "Software Engineer", 4, "Coding, System Design, Leadership, Behavioral"),
        ("Amazon", "Mid-Level", "Software Engineer", 3, "Coding, System Design, Leadership"),
        ("Amazon", "Senior", "Data Engineer", 4, "Coding, Data Modeling, SQL, Behavioral"),
        ("Microsoft", "Fresher", "Software Engineer", 3, "Coding, System Design, Behavioral"),
        ("Microsoft", "Mid-Level", "AI Engineer", 4, "Coding, AI Fundamentals, Research Discussion, Behavioral"),
        ("Netflix", "Senior", "Software Architect", 5, "Coding, System Design, Architecture Review, Leadership, Behavioral"),
        ("Tesla", "Mid-Level", "Embedded Systems Engineer", 3, "Coding, Embedded Systems, Behavioral"),
    ]

    # Insert sample data
    cursor.executemany("""
        INSERT INTO interview_stages (company_name, experience_level, role, num_rounds, round_details)
        VALUES (?, ?, ?, ?, ?)
    """, sample_data)

    conn.commit()
    conn.close()
    print("Database initialized and sample data inserted successfully.")

# Run the function to insert data
init_db()
