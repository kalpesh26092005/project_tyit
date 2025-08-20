import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("registration.html")

@app.route('/symptoms')
def symptoms():
    return render_template('symptoms.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')




# Load API key from environment variables for security
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise EnvironmentError("Please set the GOOGLE_API_KEY environment variable")

genai.configure(api_key=api_key)

# Define the system instruction for the model
system_instruction = """You are a doctor. You must only reply to health-related questions.

You must solve queries, questions, and problems in an accurate and simple way.

You must not reply to any other topic or question.

If you are asked about anything else, just say 'I am a doctor, I can only answer health-related questions.'

Else if a user asks about health-related problems, you must reply in a very polite, simple, and easy-to-understand way."""

# Initialize the model with system instruction
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)


@app.route('/ai')
def ai():
    return render_template('ai.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '')
        if not question:
            return jsonify({"error": "No question provided"}), 400

        chat = model.start_chat(history=[])
        response = chat.send_message(question)

        return jsonify({"response": response.text})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
