from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
import os

# Get the absolute path to the CSV file
csv_file_path = os.path.join(os.path.dirname(__file__), 'test.csv')

# Load and preprocess CSV
df = pd.read_csv(csv_file_path)

app = Flask(__name__)

# Load and preprocess CSV
df = pd.read_csv('test.csv')

# Optional: Clean or shuffle
df = df.sample(frac=1).reset_index(drop=True)  # Shuffle if needed

@app.route('/get-question', methods=['POST'])
def get_question():
    difficulty = int(request.json['difficulty'])
    questions = df[df['difficulty'] == difficulty]

    if questions.empty:
        return jsonify({'error': 'No questions at this difficulty'}), 404

    question = questions.sample(1).iloc[0]

    return jsonify({
        'scenario': question['scenario'],
        'options': [question['option1'], question['option2'], question['option3'], question['option4']],
        'answer': question['answer'],
        'difficulty': int(question['difficulty'])
    })

@app.route('/submit-score', methods=['POST'])
def submit_score():
    data = request.json
    name = data['name']
    points = data['points']
    # You could store this in a file or database here
    print(f"Name: {name}, Score: {points}")
    return jsonify({'status': 'Score submitted!'})

if __name__ == '__main__':
    app.run(debug=True)