import sqlite3

import pandas as pd
import streamlit as st

def show_sessions():
    conn = sqlite3.connect("./interview.db")
    df = pd.read_sql_query("SELECT * FROM interview_sessions", conn)
    st.dataframe(df)
    conn.close()

def show_rounds():
    conn = sqlite3.connect("./interview.db")
    df = pd.read_sql_query("SELECT * FROM round_performance", conn)
    st.dataframe(df)
    conn.close()

def show_questions_feedback():
    conn = sqlite3.connect("./interview.db")
    df = pd.read_sql_query("SELECT * FROM interview_questions", conn)
    st.dataframe(df)
    conn.close()

def drop_sessions():
    conn = sqlite3.connect("./interview.db")
    conn.execute("DELETE FROM interview_sessions")
    conn.commit()  # Commit the changes
    conn.close()
    st.success("All records from interview_sessions table have been deleted.")

def drop_rounds():
    conn = sqlite3.connect("./interview.db")
    conn.execute("DELETE FROM round_performance")
    conn.commit()  # Commit the changes
    conn.close()
    st.success("All records from round_performance table have been deleted.")


# drop_sessions()

show_questions_feedback()
show_sessions()
show_rounds()