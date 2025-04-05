import sqlite3

def init_db():
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    # Create interview stages table
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

    # Create round durations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS round_durations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            round_type TEXT UNIQUE,
            duration INTEGER
        )
    """)

    # Sample interview data
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

    # Sample round durations
    round_durations = [
        ("Coding", 30),
        ("System Design", 45),
        ("Behavioral", 30),
        ("ML Concepts", 40),
        ("System Thinking", 40),
        ("Leadership", 35),
        ("Data Modeling", 40),
        ("SQL", 30),
        ("AI Fundamentals", 40),
        ("Research Discussion", 45),
        ("Architecture Review", 50),
        ("Embedded Systems", 40),
    ]

    # Insert sample interview data
    cursor.executemany("""
        INSERT INTO interview_stages (company_name, experience_level, role, num_rounds, round_details)
        VALUES (?, ?, ?, ?, ?)
    """, sample_data)

    # Insert round durations (ignoring duplicates)
    cursor.executemany("""
        INSERT OR IGNORE INTO round_durations (round_type, duration)
        VALUES (?, ?)
    """, round_durations)

    conn.commit()
    conn.close()
    print("Database initialized and sample data inserted successfully.")

# Run the function to insert data
init_db()
