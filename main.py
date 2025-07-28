import streamlit as st
import sqlite3
import speech_recognition as sr
import pyttsx3
import ollama

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()


# Database setup
def init_db():
    conn = sqlite3.connect("performance.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            user_response TEXT,
            ai_feedback TEXT
        )
    """)
    conn.commit()
    conn.close()


# Function to ask a question
def ask_question():
    response = ollama.chat(model="gemma:2b", messages=[
        {"role": "system", "content": "Generate an interview question for a software engineer."}])
    question = response["message"]["content"]
    st.session_state["current_question"] = question
    tts_engine.say(question)
    tts_engine.runAndWait()
    return question


# Function to record response
def record_response():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Click 'Stop Recording' to end.")
        full_response = []
        st.session_state["listening"] = True

        while st.session_state.get("listening", False):
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                response_text = recognizer.recognize_google(audio)
                full_response.append(response_text)
            except sr.UnknownValueError:
                st.write("Could not understand audio.")
            except sr.RequestError:
                st.write("Speech recognition service error.")

        return " ".join(full_response)


# Function to stop listening
def stop_listening():
    st.session_state["listening"] = False


# Function to analyze response
def analyze_response(response_text):
    response = ollama.chat(model="gemma:2b", messages=[
        {"role": "system", "content": f"Evaluate this interview response: {response_text}"}])
    feedback = response["message"]["content"]
    return feedback


# Store in database
def save_to_db(question, response, feedback):
    conn = sqlite3.connect("performance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO responses (question, user_response, ai_feedback) VALUES (?, ?, ?)",
                   (question, response, feedback))
    conn.commit()
    conn.close()


# Streamlit UI
st.title("AI Interview Coach")
init_db()

if "current_question" not in st.session_state:
    if st.button("Start Interview"):
        st.session_state["current_question"] = ask_question()

if "current_question" in st.session_state:
    st.write(f"**Question:** {st.session_state['current_question']}")
    if st.button("Start Recording"):
        response = record_response()
        st.session_state["recorded_response"] = response

    if st.button("Stop Recording"):
        stop_listening()

    if "recorded_response" in st.session_state:
        st.write(f"**Your Answer:** {st.session_state['recorded_response']}")
        feedback = analyze_response(st.session_state['recorded_response'])
        st.write(f"**AI Feedback:** {feedback}")
        save_to_db(st.session_state["current_question"], st.session_state['recorded_response'], feedback)
        del st.session_state["current_question"]
        del st.session_state["recorded_response"]
