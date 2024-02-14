# app.py

from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Function to generate questions
def generate_question():
    payouts = {
        'straight': 35,  # Betting on a single number
        'split': 17,     # Betting on two adjacent numbers
        'street': 11,    # Betting on three numbers in a row
        'corner': 8,     # Betting on four numbers that form a square
        'six_line': 5,   # Betting on six numbers from two adjacent rows
    }
    bet_type = random.choice(list(payouts.keys()))
    amount = random.randint(1, 20)
    correct_answer = payouts[bet_type] * amount
    return bet_type, amount, correct_answer

# Global variables to keep track of score and current question
correct_answers = 0
wrong_answers = 0
current_question = generate_question()
user_name = None

# Route to ask for user's name and start quiz
@app.route('/', methods=['GET', 'POST'])
def index():
    global user_name
    if request.method == 'POST':
        user_name = request.form.get('name')
        return redirect(url_for('quiz'))  # Redirect to the quiz route
    return render_template('index.html')

# Route to start the quiz
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global current_question, correct_answers, wrong_answers
    if request.method == 'POST':
        user_answer = request.form.get('user_answer')
        if user_answer is not None and user_answer.isdigit():
            if int(user_answer) == current_question[2]:
                correct_answers += 1
            else:
                wrong_answers += 1
        current_question = generate_question()
    return render_template('quiz.html', question=current_question)

# Route for showing answers
@app.route('/show_answers')
def show_answers():
    return render_template('show_answers.html', name=user_name, correct=correct_answers, wrong=wrong_answers)

if __name__ == '__main__':
    app.run(debug=True)
