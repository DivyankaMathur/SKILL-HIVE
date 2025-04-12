from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get the OpenAI API key from the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_career_advice", methods=["POST"])
def get_career_advice():
    data = request.get_json()

    # Check if required fields exist, otherwise return an error response
    if not data.get('age') or not data.get('work_style') or not data.get('work_env') or not data.get('work_type'):
        return jsonify({"error": "Missing required fields. Please provide age, work style, work environment, and work type."}), 400

    # Construct the prompt for OpenAI model
    prompt = f"""
    You are a career counselor. Suggest a career for someone with the following profile:

    Age: {data.get('age')}
    Work Style: {data.get('work_style')}
    Work Environment: {data.get('work_env')}
    Work Type: {data.get('work_type')}
    Activities: {', '.join(data.get('fav_activities', [])) if data.get('fav_activities') else 'Not provided'}
    Strengths: {', '.join(data.get('strengths', [])) if data.get('strengths') else 'Not provided'}
    """

    try:
        # Get response from OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful and insightful career guidance expert."},
                      {"role": "user", "content": prompt}]
        )

        # Extract career suggestion from the response
        suggestion = response['choices'][0]['message']['content'].strip()
        
        return jsonify({"career": suggestion})

    except Exception as e:
        # Log the error for debugging
        print(f"Error: {str(e)}")
        return jsonify({"error": "An error occurred while processing the request. Please try again later."}), 500

if __name__ == "__main__":
    app.run(debug=True)
