from flask import Flask, request, jsonify
from flask_cors import CORS
from data_loader import DataLoader
from model import DiseasePredictor
from chatbot import HealthcareChatbot
import pandas as pd
import re
import pyttsx3
import random

app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app)  # Enable CORS for frontend communication

# Initialize chatbot components
data_loader = DataLoader()
data_loader.load_descriptions()
data_loader.load_severity()
data_loader.load_precautions()
training_data = data_loader.load_training_data()
reduced_data = training_data.groupby(training_data['prognosis']).max()
X = training_data.drop('prognosis', axis=1)
y = training_data['prognosis']
predictor = DiseasePredictor()
metrics = predictor.train(X, y)
chatbot = HealthcareChatbot(data_loader, predictor, reduced_data)

# Store conversation state for each session
sessions = {}

# Singleton pyttsx3 engine for text-to-speech
engine = None

def init_engine():
    """Initialize the pyttsx3 engine as a singleton."""
    global engine
    if engine is None:
        engine = pyttsx3.init()
        engine.setProperty('voice', "english+f5")
        engine.setProperty('rate', 130)
    return engine

def speak(text):
    """Speak text using pyttsx3, handling potential run loop errors."""
    try:
        engine = init_engine()
        engine.say(text)
        engine.runAndWait()
    except RuntimeError as e:
        print(f"Text-to-speech error: {e}")
        # Continue without crashing; audio fails silently
        pass

@app.route('/')
def serve_frontend():
    """Serve the React frontend."""
    return app.send_static_file('index.html')

@app.route('/start', methods=['POST'])
def start_chat():
    """Start a new conversation session."""
    session_id = request.json.get('session_id', 'default')
    name = request.json.get('name', '')
    sessions[session_id] = {
        'step': 'symptom',
        'name': name,
        'symptoms_exp': [],
        'num_days': 0,
        'questions_asked': 0,
        'max_questions': 5,
        'available_symptoms': list(chatbot.symptoms),
        'symptoms_present': []
    }
    response = f"Hello, {name}\nEnter the symptom you are experiencing:"
    if request.json.get('audio', True):
        speak(response)
    return jsonify({
        'message': response,
        'step': 'symptom',
        'cross_val_score': metrics['cross_val_score'] * 100
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat interactions based on conversation step."""
    session_id = request.json.get('session_id', 'default')
    user_input = request.json.get('input', '').lower()
    audio = request.json.get('audio', True)
    if session_id not in sessions:
        return jsonify({'error': 'Session not found'}), 400

    state = sessions[session_id]
    response = []
    step = state['step']

    if step == 'symptom':
        chk_dis = ",".join(chatbot.symptoms).split(",")
        conf, cnf_dis = chatbot.check_pattern(chk_dis, user_input)
        if conf == 1:
            state['possible_symptoms'] = cnf_dis
            if len(cnf_dis) > 1:
                response.append("Searches related to input:")
                for num, sym in enumerate(cnf_dis):
                    response.append(f"{num} ) {sym}")
                response.append(f"Select the one you meant (0 - {len(cnf_dis)-1}):")
                state['step'] = 'select_symptom'
            else:
                state['symptoms_exp'].append(cnf_dis[0])
                response.append("Okay. From how many days ?")
                state['step'] = 'days'
        else:
            response.append("Enter valid symptom.")

    elif step == 'select_symptom':
        try:
            index = int(user_input)
            if 0 <= index < len(state['possible_symptoms']):
                state['symptoms_exp'].append(state['possible_symptoms'][index])
                response.append("Okay. From how many days ?")
                state['step'] = 'days'
            else:
                response.append(f"Select a valid number (0 - {len(state['possible_symptoms'])-1}):")
        except ValueError:
            response.append("Enter a valid number.")

    elif step == 'days':
        try:
            num_days = int(user_input)
            state['num_days'] = num_days
            state['step'] = 'follow_up'
            # Start asking random symptom questions
            response.extend(ask_random_symptom(session_id))
        except ValueError:
            response.append("Enter a valid number of days.")

    elif step == 'follow_up':
        symptom = state.get('current_symptom')
        state['symptoms_present'].append(symptom)
        state['questions_asked'] += 1

        # Heuristic to interpret flexible responses
        positive_indicators = ['yes', 'yeah', 'sometimes', 'did', 'have']
        negative_indicators = ['no', 'never', 'not']
        if any(indicator in user_input for indicator in positive_indicators):
            state['symptoms_exp'].append(symptom)
            response.append(f"Okay, I’ll note that you are experiencing {symptom}. ")
        elif any(indicator in user_input for indicator in negative_indicators):
            response.append(f"Got it, you’re not experiencing {symptom}. ")
        else:
            response.append(f"I’m not sure what you mean by '{user_input}'. I’ll assume no for now. ")

        # Ask the next random symptom or make prediction
        if state['questions_asked'] < state['max_questions']:
            response.extend(ask_random_symptom(session_id))
        else:
            response.extend(make_prediction(session_id))
            state['step'] = 'complete'

    message = "\n".join(response) if response else "No more questions."
    if message and audio:
        speak(message)
    return jsonify({'message': message, 'step': state['step']})

def ask_random_symptom(session_id):
    """Ask a random symptom question and update state."""
    state = sessions[session_id]
    if not state['available_symptoms']:
        state['available_symptoms'] = list(chatbot.symptoms)  # Reset if exhausted
    symptom = random.choice(state['available_symptoms'])
    state['available_symptoms'].remove(symptom)
    state['current_symptom'] = symptom
    return [f"Are you experiencing {symptom}?"]
def make_prediction(session_id):
    """Make a prediction based on collected symptoms."""
    state = sessions[session_id]
    description_list = data_loader.load_descriptions()
    precaution_dict = data_loader.load_precautions()
    severity_dict = data_loader.load_severity()

    # Calculate severity
    sum_severity = sum(severity_dict.get(item, 0) for item in state['symptoms_exp'])
    severity_score = (sum_severity * state['num_days']) / (len(state['symptoms_exp']) + 1)
    if severity_score > 13:
        response = ["You should take the consultation from doctor."]
    else:
        response = ["It might not be that bad but you should take precautions."]

    # Prediction
    prediction = predictor.predict(state['symptoms_exp'])
    response.append(f"You may have {prediction}")
    response.append(description_list.get(prediction, "Description not available"))

    # Precautions
    precaution_list = precaution_dict.get(prediction, [])
    response.append("Take following measures:")
    for i, precaution in enumerate(precaution_list, 1):
        if precaution:
            response.append(f"{i}) {precaution}")

    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)