import csv
import json

def convert_csv_to_json(csv_file_path, json_file_path):
    questions = []

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append({
                "scenario": row["question"],     # change from 'scenario' to 'question'
                "options": [row["option1"], row["option2"]],
                "correct": row["correct"]
            })

    with open(json_file_path, "w", encoding='utf-8') as jsonfile:
        json.dump(questions, jsonfile, indent=2)

# 👇 Call this function to actually run the conversion
convert_csv_to_json("test.csv", "test.json")
