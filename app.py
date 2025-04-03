import streamlit as st
import sqlite3

from utils.aiHelper import fetch_interview_rounds, generate_question, evaluate_response

st.title("AI Interview Coach")

if "user_answer" not in st.session_state:
    st.session_state["user_answer"] = ""

def get_interview_rounds(company, experience, role):
    conn = sqlite3.connect("./database/interview.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT num_rounds, round_details 
        FROM interview_stages 
        WHERE company_name = ? AND experience_level = ? AND role = ?
    """, (company, experience, role))

    result = cursor.fetchone()
    conn.close()

    if result:
        num_rounds, round_details = result
        return num_rounds, round_details.split(", ")  # Convert string to list
    else:
        return None, None  # No data found

# Submit button callback
def submit_response():
    if st.session_state.get("user_answer", "").strip():  # Ensure the answer is not empty
        st.session_state["submitted"] = True
        st.session_state["saved_answer"] = st.session_state["user_answer"]  # Only save when submitted
        st.session_state["user_answer"] = ''
    else:
        st.error("❌ Your response is too short. Please provide a more detailed answer.")

# User selects company, experience level, and role
company = st.selectbox("Select Company", ["Google", "Meta", "Amazon", "Microsoft", "Netflix", "Tesla"])
experience_levels = {
    "Fresher (0-1 years)": "Fresher",
    "Junior (1-3 years)": "Junior",
    "Mid-Level (3-7 years)": "Mid-Level",
    "Senior (7-12 years)": "Senior",
    "Principal/Lead (12+ years)": "Principal"
}
experience = st.selectbox("Select Experience Level", list(experience_levels.keys()))
role = st.selectbox("Select Role",
                    ["Software Engineer", "Data Scientist", "Data Engineer", "AI Engineer", "Software Architect",
                     "Embedded Systems Engineer"])

# Fetch and display interview rounds
if st.button("Fetch Interview Rounds"):
    mapped_experience = experience_levels[experience]  # Map to DB-compatible value
    num_rounds, round_types = get_interview_rounds(company, mapped_experience, role)
    if num_rounds:
        st.session_state["rounds"] = round_types
        st.session_state["current_round"] = -1  # Initialize before starting
        st.session_state["feedback_shown"] = True  # Track if feedback is displayed
        st.success(f"Fetched {int(num_rounds)} rounds for {role} at {company}. Click 'Start Interview' to begin.")
        st.success(f"**Rounds:** {', '.join(round_types)}")
    else:
        st.write("No interview data found for this selection.")

if "rounds" in st.session_state and st.session_state["rounds"]:
    if st.session_state["current_round"] == -1:
        if st.button("Start Interview"):
            st.session_state["current_round"] = 0
            st.session_state["feedback_shown"] = False
            st.session_state["question_index"] = 0
            st.rerun()

    elif st.session_state["current_round"] < len(st.session_state["rounds"]):
        round_type = st.session_state["rounds"][st.session_state["current_round"]]
        st.subheader(f"Round {st.session_state['current_round'] + 1}: {round_type}")

        question = generate_question(role, experience, company, round_type)
        st.write("**Question:**", question)
        user_answer = st.text_area("Your Answer:", key='user_answer')

        if "submitted" not in st.session_state:
            st.session_state["submitted"] = False
        if "saved_answer" not in st.session_state:
            st.session_state["saved_answer"] = ""

        # Submit button
        st.button("Submit Answer", on_click=submit_response)

        # Process the answer ONLY IF the submit button was clicked
        if st.session_state["submitted"]:
            score, feedback = evaluate_response(question, st.session_state["saved_answer"])

            st.session_state["feedback_shown"] = True
            st.session_state["score"] = score
            st.session_state["feedback"] = feedback

            st.write(f"**Score:** {score}/10")
            st.info(f"**Feedback:** {feedback}")

            # Reset submitted state so that the user can submit again for the next question
            st.session_state["submitted"] = False
            # st.session_state["user_answer"] = ""  # This clears the text area
            st.rerun()

        if st.session_state.get("feedback_shown", False):
            next_button = st.button("Next Question")
            if next_button:
                st.session_state["feedback_shown"] = False
                st.session_state["score"] = None
                st.session_state["feedback"] = None
                st.rerun()
        if st.button("Next Round"):
            st.session_state["current_round"] += 1
            st.session_state["feedback_shown"] = False
            st.rerun()
        if st.session_state["current_round"] >= len(st.session_state["rounds"]):
            st.balloons()
            st.success("🎉 Congratulations! You completed all rounds.")
            del st.session_state["rounds"]
            del st.session_state["current_round"]
            del st.session_state["feedback_shown"]