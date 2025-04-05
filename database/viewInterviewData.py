import sqlite3


def fetch_interview_data():
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM interview_stages")
    records = cursor.fetchall()

    for record in records:
        print(record)

    conn.close()

def fetch_duration_data():
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    query = """
        SELECT 
            isg.company_name, 
            isg.experience_level, 
            isg.role, 
            isg.num_rounds, 
            isg.round_details, 
            COALESCE((
                SELECT SUM(rd.duration)
                FROM round_durations rd
                WHERE ',' || isg.round_details || ',' LIKE '%,' || rd.round_type || ',%'
            ), 0) AS total_duration
        FROM interview_stages isg
        GROUP BY isg.id
    """

    cursor.execute(query)
    records = cursor.fetchall()

    # Print the records in a structured way
    print("\nInterview Rounds Data:")
    print("-" * 110)
    print(f"{'Company':<15}{'Experience':<12}{'Role':<25}{'Rounds':<8}{'Round Details':<50}{'Total Duration (min)':<5}")
    print("-" * 110)

    for record in records:
        print(f"{record[0]:<15}{record[1]:<12}{record[2]:<25}{record[3]:<8}{record[4]:<50}{record[5]:<5}")

    conn.close()


fetch_interview_data()

fetch_duration_data()
