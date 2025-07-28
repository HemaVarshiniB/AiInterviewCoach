import ollama
import json
import re
import requests
import tempfile
import playsound  # pip install playsound==1.2.2


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
        question = response.message.content.strip()
        speak_with_vapi(
            text=question,
            voice_id="voice_olivia_us",
            api_key="3cb0ead9-07b7-4ad5-98a3-651cf8792d5e"
        )
        return question
    else:
        return f"Error: Unable to extract content from response. Full response: {response}"


# Function to evaluate response using Ollama
def evaluate_response(question, user_response):
    prompt = f"Evaluate the following response for the question: '{question}'\nResponse: '{user_response}'\nGive a score out of 10 and provide feedback."

    # Call Ollama LLM (adjust model as needed)
    response = ollama.chat(model="gemma:2b", messages=[{"role": "user", "content": prompt}])
    evaluation = response['message']['content']

    # Extract score using regex to handle potential score format issues
    score_match = re.search(r"Score:\s*(\d+(\.\d+)?)", evaluation)  # Regex to capture score (integer or float)
    if score_match:
        score = float(score_match.group(1))  # Convert to float first
        score = int(score)  # Convert to integer
    else:
        score = 5  # Default fallback score if not found

    # Extract feedback (assuming 'Feedback:' keyword is present in the response)
    feedback = evaluation.split("Feedback:")[1].strip() if "Feedback:" in evaluation else evaluation

    return score, feedback

def speak_with_vapi(text, voice_id, api_key):
    url = "https://api.vapi.ai/api/text-to-speech"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_id": voice_id,
        "output_format": "mp3"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        audio_url = response.json().get("audio_url")

        # Download and play the audio
        audio_data = requests.get(audio_url).content
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(audio_data)
            f.flush()
            playsound.playsound(f.name)
    else:
        print("Failed to generate audio:", response.text)

