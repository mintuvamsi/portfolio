from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample questions about roulette
roulette_questions = [
    "What is the origin of Russian roulette?",
    "How many chambers are typically in a revolver used for Russian roulette?",
    "Why is playing Russian roulette dangerous?",
    "What are some alternatives to Russian roulette for entertainment?"
]

@app.route('/questions', methods=['GET'])
def get_question():
    # Check if 'index' parameter is provided in the request
    question_index = request.args.get('index')

    if question_index is None:
        return jsonify({"error": "Please provide 'index' parameter."}), 400
    
    # Convert 'index' parameter to integer
    try:
        question_index = int(question_index)
    except ValueError:
        return jsonify({"error": "'index' parameter must be an integer."}), 400
    
    # Check if the index is valid
    if question_index < 0 or question_index >= len(roulette_questions):
        return jsonify({"error": "Invalid question index."}), 400
    
    # Return the question at the specified index
    return jsonify({"question": roulette_questions[question_index]})

if __name__ == '__main__':
    app.run(debug=True)
