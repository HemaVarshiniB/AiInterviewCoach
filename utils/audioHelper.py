from transformers import pipeline
import speech_recognition as sr
import pyttsx3
import streamlit as st
import threading

# Load HuggingFace model for text generation (DialoGPT)
chatbot = pipeline('text-generation', model='microsoft/DialoGPT-medium')

# Speech-to-text function
def listen_to_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while st.session_state.listening:
            st.write("Listening for your answer...")
            audio = recognizer.listen(source)
            try:
                user_input = recognizer.recognize_google(audio)
                st.write(f"You said: {user_input}")
                # Get model's response
                bot_response = chatbot(user_input, max_length=1000, num_return_sequences=1)
                response_text = bot_response[0]['generated_text']
                st.write(f"AI Response: {response_text}")

                # Convert model's response to speech
                text_to_speech(response_text)
            except sr.UnknownValueError:
                st.write("Sorry, I could not understand.")
            except sr.RequestError:
                st.write("Sorry, there was an issue with the speech recognition service.")

# Text-to-speech function
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Start listening function
def start_listening():
    st.session_state.listening = True
    st.write("Started listening...")
    listen_to_speech()

# Stop listening function
def stop_listening():
    st.session_state.listening = False
    st.write("Stopped listening.")

# Main app logic
def main():
    st.title("AI Interview Coach")

    # Initialize session state for listening
    if 'listening' not in st.session_state:
        st.session_state.listening = False

    # Start Listening button
    if st.button("Start Listening"):
        if not st.session_state.listening:
            threading.Thread(target=start_listening).start()  # Run listening in a separate thread to keep UI responsive

    # Stop Listening button
    if st.button("Stop Listening"):
        stop_listening()

if __name__ == "__main__":
    main()