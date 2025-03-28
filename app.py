import streamlit as st
from aiHelper import fetch_interview_rounds, generate_question, evaluate_response

st.title("AI Interview Coach")

# Get user input
# candidate_name = st.text_input("Enter your name:")
company = st.text_input("Enter the company you're applying to:")
role = st.text_input("Enter the role you're applying for:")
experience = st.slider("Years of experience:", 0, 20, 2)

# Fetch interview rounds
if st.button("Fetch Interview Rounds"):
    interview_rounds = fetch_interview_rounds(company, role)

    if interview_rounds:
        st.session_state["rounds"] = interview_rounds
        st.session_state["current_round"] = -1  # Set to -1, will be updated when "Start Interview" is clicked
        st.success(f"Fetched {len(interview_rounds)} rounds for {role} at {company}. Click 'Start Interview' to begin.")
    else:
        st.error("Could not fetch interview rounds. Try again.")

# Start Interview Button
if "rounds" in st.session_state and st.session_state["rounds"]:
    if st.session_state["current_round"] == -1:
        if st.button("Start Interview"):
            st.session_state["current_round"] = 0
            st.rerun()  # ✅ Fixed rerun issue

    elif st.session_state["current_round"] < len(st.session_state["rounds"]):
        round_info = st.session_state["rounds"][st.session_state["current_round"]]
        round_name, round_type = round_info["round"], round_info["type"]

        st.subheader(f"Round {st.session_state['current_round'] + 1}: {round_name} ({round_type})")

        question = generate_question(role, experience, company, round_type)
        st.write("Question:", question)

        user_answer = st.text_area("Your Answer:")
        print("FEEDBACK:: ", evaluate_response(question, user_answer))
        if st.button("Submit Answer"):
            if len(user_answer) > 20:  # Simple pass/fail logic
                st.success("✅ You passed this round!")
                st.session_state["current_round"] += 1
            else:
                st.error("❌ You did not pass. Try again.")

            if st.session_state["current_round"] >= len(st.session_state["rounds"]):
                st.balloons()
                st.success("🎉 Congratulations! You completed all rounds.")
                del st.session_state["rounds"]
                del st.session_state["current_round"]
