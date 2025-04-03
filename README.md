**AI Interview Coach**

Purpose: The AI Interview Coach project aims to assist job seekers, particularly those applying for software engineering roles at companies in enhancing their interview skills through AI-driven mock interviews. The system will simulate real interview scenarios by asking role-specific questions, analyzing candidate responses in real time, and providing constructive feedback.

*Installation & Launching:*
1. Setup Virtual env => to activate it follow this cmd => *.venv\Scripts\activate* (for windows)
2. Install necessary libraries through pip. (ollama, gemma:2b, streamlit, sqlite3)
3. Launch application with this cmd => *streamlit run app.py*
4. To create sqlite3 db and insert records in db, go to interviewStages.py path and run cmd => *streamlit run interviewStages.py*. This will create db and tables in it.
