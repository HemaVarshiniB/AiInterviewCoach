import ollama
import json


def fetch_interview_rounds(company, role):
    """Prompt AI to determine interview rounds based on company and role."""
    prompt = f"""
    You are an AI assistant that provides interview details for a given company and role.
    The user is applying for the **{role}** position at **{company}**.

    Provide a JSON array of interview rounds in the following format:
    [
        {{"round": "Round Name", "type": "Round Type"}},
        {{"round": "Round Name", "type": "Round Type"}}
    ]

    Example:
    If the role is 'Software Engineer' at Google, your response might be:
    [
        {{"round": "Online Assessment", "type": "DSA"}},
        {{"round": "Technical Interview 1", "type": "DSA"}},
        {{"round": "System Design Interview", "type": "System Design"}},
        {{"round": "Behavioral Interview", "type": "Behavioral"}}
    ]

    Only provide a valid JSON response without additional text.
    """

    response = ollama.chat(model="gemma:2b", messages=[{"role": "system", "content": prompt}])

    try:
        rounds = json.loads(response["message"]["content"])  # Convert JSON string to Python list
        return rounds
    except json.JSONDecodeError:
        return []  # Return empty list if parsing fails


def generate_question(role, experience, company, round_type):
    prompt = f"""
    I am preparing for an interview as a {role} at {company}. I have {experience} years of experience.
    Please generate a relevant question based on the following round type:

    Round Type: {round_type}

    Please provide one question based on the given information. The question should be:
    - For 'Technical' rounds, focus on coding challenges, algorithms, data structures, or problem-solving skills.
    - For 'Behavioral' rounds, provide a question that assesses soft skills, teamwork, leadership, or communication.
    - For 'System Design' rounds, provide a question that involves designing scalable systems, choosing appropriate technologies, and explaining architecture.
    - For 'Data Structures and Algorithms' (DSA) rounds, focus on questions that test knowledge of algorithms, sorting, searching, dynamic programming, graphs, etc.
    """

    # Send the request to the model
    response = ollama.chat(model="gemma:2b", messages=[{"role": "system", "content": prompt}])

    # Debug: Print the full response
    print("Response from Ollama:", response)

    # Correct way to access content
    if response and hasattr(response, "message") and hasattr(response.message, "content"):
        return response.message.content.strip()
    else:
        return f"Error: Unable to extract content from response. Full response: {response}"


# Function to evaluate response using Ollama
def evaluate_response(question, user_response):
    prompt = f"Evaluate the following response for the question: '{question}'\nResponse: '{user_response}'\nGive a score out of 10 and provide feedback."

    # Call Ollama LLM (adjust model as needed)
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    evaluation = response['message']['content']

    # Extract score and feedback (assuming LLM returns structured response)
    score = int(evaluation.split("Score:")[1].split("\n")[0].strip()) if "Score:" in evaluation else 5
    feedback = evaluation.split("Feedback:")[1].strip() if "Feedback:" in evaluation else evaluation

    return score, feedback