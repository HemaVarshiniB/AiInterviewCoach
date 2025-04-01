import streamlit as st
from aiHelper import fetch_interview_rounds, generate_question, evaluate_response

st.title("AI Interview Coach")

# Get user input
company = st.text_input("Enter the company you're applying to:")
role = st.text_input("Enter the role you're applying for:")
experience = st.slider("Years of experience:", 0, 20, 2)

# Fetch interview rounds
if st.button("Fetch Interview Rounds"):
    interview_rounds = fetch_interview_rounds(company, role)

    if interview_rounds:
        st.session_state["rounds"] = interview_rounds
        st.session_state["current_round"] = -1  # Initialize before starting
        st.session_state["feedback_shown"] = True  # Track if feedback is displayed
        st.success(f"Fetched {len(interview_rounds)} rounds for {role} at {company}. Click 'Start Interview' to begin.")
    else:
        st.error("Could not fetch interview rounds. Try again.")

# Start Interview Button
if "rounds" in st.session_state and st.session_state["rounds"]:
    if st.session_state["current_round"] == -1:
        if st.button("Start Interview"):
            st.session_state["current_round"] = 0
            st.session_state["feedback_shown"] = False  # Feedback not shown initially
            st.session_state["question_index"] = 0  # Track which question we are on in the round
            st.rerun()  # Ensure the UI updates properly

    elif st.session_state["current_round"] < len(st.session_state["rounds"]):
        round_info = st.session_state["rounds"][st.session_state["current_round"]]
        round_name, round_type = round_info["round"], round_info["type"]

        st.subheader(f"Round {st.session_state['current_round'] + 1}: {round_name} ({round_type})")

        question = generate_question(role, experience, company, round_type)

        # Display the question
        st.write("Question:", question)
        user_answer = st.text_area("Your Answer:")

        # Process Answer and evaluate feedback
        if st.button("Submit Answer") and user_answer:
            if len(user_answer) > 0:  # Simple check for minimum answer length
                score, feedback = evaluate_response(question, user_answer)
                print(score, feedback)

                # Extract only the first part if score is in 'x/y' format
                if isinstance(score, str) and '/' in score:
                    score = int(score.split('/')[0].strip())

                # Store feedback in session state
                st.session_state["feedback_shown"] = True  # Feedback should be shown now
                st.session_state["score"] = score
                st.session_state["feedback"] = feedback

                # Display feedback
                st.write(f"**Score:** {score}/10")
                st.info(f"**Feedback:** {feedback}")

            else:
                st.error("❌ Your response is too short. Please provide a more detailed answer.")

        # Show 'Next Question' button only after feedback is displayed
        if st.session_state.get("feedback_shown", False):
            next_button = st.button("Next Question")

            if next_button:
                # Move to the next question in the same round
                st.session_state["feedback_shown"] = False  # Reset feedback flag for next question
                st.session_state["score"] = None  # Clear score for the next question
                st.session_state["feedback"] = None  # Clear feedback for the next question
                st.rerun()  # Update the UI with the next question

        # End of round logic: Proceed to the next round once all questions in the current round are answered
        if st.button("Next Round"):
            st.session_state["current_round"] += 1  # Proceed to the next round
            st.session_state["feedback_shown"] = False  # Reset feedback flag for the next round
            st.rerun()  # Update the UI to show the next round

        # Completion Message
        if st.session_state["current_round"] >= len(st.session_state["rounds"]):
            st.balloons()
            st.success("🎉 Congratulations! You completed all rounds.")
            # Clear session state data related to rounds and current state
            del st.session_state["rounds"]
            del st.session_state["current_round"]
            del st.session_state["feedback_shown"]




