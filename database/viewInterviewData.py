import sqlite3


def fetch_data():
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM interview_stages")
    records = cursor.fetchall()

    for record in records:
        print(record)

    conn.close()


fetch_data()
