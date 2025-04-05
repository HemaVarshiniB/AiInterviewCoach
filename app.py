import datetime

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


def get_round_duration(round_type):
    conn = sqlite3.connect("./database/interview.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT duration FROM round_durations WHERE round_type = ?
    """, (round_type,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 10  # default 10 minutes


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

if "round_ids" not in st.session_state:
    st.session_state["round_ids"] = []

if "rounds" in st.session_state and st.session_state["rounds"]:
    if st.session_state["current_round"] == -1:
        if st.button("Start Interview"):
            st.session_state["current_round"] = 0
            st.session_state["feedback_shown"] = False
            st.session_state["question_index"] = 0

            # Insert new session
            conn = sqlite3.connect("./database/interview.db")
            cursor = conn.cursor()
            interview_date = datetime.datetime.now()
            user_id = 1  #TODO: NEED TO FETCH LOOGEDIN USER

            cursor.execute("""
                    INSERT INTO interview_sessions (user_id, company_name, role, experience, interview_date, session_performance)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, company, role, experience_levels[experience], interview_date, 0))

            conn.commit()
            # Save the session_id to state
            st.session_state["session_id"] = cursor.lastrowid
            st.session_state["user_id"] = user_id

            # Insert round performance row
            round_type = st.session_state["rounds"][0]
            cursor.execute("""
                        INSERT INTO round_performance (session_id, user_id, round_type)
                        VALUES (?, ?, ?)
                    """, (st.session_state["session_id"], 1, round_type))  # user_id = 1

            round_id = cursor.lastrowid
            st.session_state["round_ids"].append(round_id)
            conn.commit()

            conn.close()

            st.rerun()

    elif st.session_state["current_round"] < len(st.session_state["rounds"]):
        round_type = st.session_state["rounds"][st.session_state["current_round"]]
        st.subheader(f"Round {st.session_state['current_round'] + 1}: {round_type}")
        round_id = st.session_state["round_ids"][st.session_state["current_round"]]

        # Track round start time and duration
        if "round_start_time" not in st.session_state or st.session_state["new_round"]:
            st.session_state["round_duration"] = get_round_duration(round_type)
            st.session_state["round_start_time"] = datetime.datetime.now()
            st.session_state["new_round"] = False

        # Check if round time is up
        elapsed = (datetime.datetime.now() - st.session_state["round_start_time"]).total_seconds()
        time_left = st.session_state["round_duration"] * 60 - elapsed

        # Show remaining time
        minutes, seconds = divmod(int(time_left), 60)
        st.info(f"🕒 Time Left in Round: {minutes:02d}:{seconds:02d}")

        if time_left <= 0:
            st.warning("⏰ Time's up for this round!")

            # Store feedback for the entire round once time is up
            round_id = st.session_state["round_ids"][st.session_state["current_round"]]
            avg_score = sum(st.session_state.get("round_scores", [])) / max(
                len(st.session_state.get("round_scores", [])), 1)
            round_feedback = "Round completed within time. Good effort!"  # This can be dynamic

            # Save feedback and score for the round in the database
            conn = sqlite3.connect("./database/interview.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE round_performance SET round_score = ?, round_feedback = ?
                WHERE round_id = ?
            """, (avg_score, round_feedback, round_id))
            conn.commit()
            conn.close()

            # Prepare next round
            st.session_state["current_round"] += 1
            st.session_state["feedback_shown"] = False
            st.session_state["round_scores"] = []
            st.session_state["new_round"] = True

            if st.session_state["current_round"] >= len(st.session_state["rounds"]):
                st.balloons()
                st.success("🎉 All rounds complete!")
                del st.session_state["rounds"]
                del st.session_state["current_round"]
                del st.session_state["feedback_shown"]
            st.rerun()

        # If there's time left, continue with the interview question
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

            # Save to round_performance table
            conn = sqlite3.connect("./database/interview.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO interview_questions (round_id, question_text, user_response, question_category, question_score, question_feedback)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (round_id, question, st.session_state["saved_answer"], round_type, score, feedback))

            conn.commit()
            conn.close()

            st.session_state["feedback_shown"] = True
            st.session_state["score"] = score
            st.session_state["feedback"] = feedback

            st.write(f"Score: {score}/10")
            st.info(f"Feedback: {feedback}")
            # Reset submitted state so that the user can submit again for the next question
            st.session_state["submitted"] = False

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


    # elif st.session_state["current_round"] < len(st.session_state["rounds"]):
    #     round_type = st.session_state["rounds"][st.session_state["current_round"]]
    #     st.subheader(f"Round {st.session_state['current_round'] + 1}: {round_type}")
    #     round_id = st.session_state["round_ids"][st.session_state["current_round"]]
    #
    #     question = generate_question(role, experience, company, round_type)
    #     st.write("**Question:**", question)
    #     user_answer = st.text_area("Your Answer:", key='user_answer')
    #
    #     if "submitted" not in st.session_state:
    #         st.session_state["submitted"] = False
    #     if "saved_answer" not in st.session_state:
    #         st.session_state["saved_answer"] = ""
    #
    #     # Submit button
    #     st.button("Submit Answer", on_click=submit_response)
    #
    #     # Process the answer ONLY IF the submit button was clicked
    #     if st.session_state["submitted"]:
    #         score, feedback = evaluate_response(question, st.session_state["saved_answer"])
    #
    #         st.session_state["feedback_shown"] = True
    #         st.session_state["score"] = score
    #         st.session_state["feedback"] = feedback
    #
    #         st.write(f"Score: {score}/10")
    #         st.info(f"Feedback: {feedback}")
    #         # Reset submitted state so that the user can submit again for the next question
    #         st.session_state["submitted"] = False
    #         # st.session_state["user_answer"] = ""  # This clears the text area
    #
    #         # Save to round_performance table
    #         conn = sqlite3.connect("./database/interview.db")
    #         cursor = conn.cursor()
    #
    #         cursor.execute("""
    #                 INSERT INTO interview_questions (round_id, question_text, question_category, question_score, question_feedback)
    #                 VALUES (?, ?, ?, ?, ?)
    #             """, (round_id, question, round_type, score, feedback))
    #
    #         conn.commit()
    #         conn.close()
    #
    #         st.rerun()
    #
    #     if st.session_state.get("feedback_shown", False):
    #         next_button = st.button("Next Question")
    #         if next_button:
    #             st.session_state["feedback_shown"] = False
    #             st.session_state["score"] = None
    #             st.session_state["feedback"] = None
    #             st.rerun()
    #     if st.button("Next Round"):
    #         st.session_state["current_round"] += 1
    #         st.session_state["feedback_shown"] = False
    #         st.rerun()
    #     if st.session_state["current_round"] >= len(st.session_state["rounds"]):
    #         st.balloons()
    #         st.success("🎉 Congratulations! You completed all rounds.")
    #         del st.session_state["rounds"]
    #         del st.session_state["current_round"]
    #         del st.session_state["feedback_shown"]
