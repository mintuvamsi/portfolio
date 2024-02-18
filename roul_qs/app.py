from flask import Flask, render_template, request, redirect, url_for
import random
import os
import psycopg2
from qs import *
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('roul_qs/db.INI')
print(type(config['db_connection']['host']))

# Function to establish a database connection


def get_db_connection():
    conn = psycopg2.connect(
        host=(config['db_connection']['host']),
        database=(config['db_connection']['database']),
        user=(config['db_connection']['user']),
        password=(config['db_connection']['password'])
    )
    return conn

# Function to create the quiz_answers table if it doesn't exist


def create_quiz_answers_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_answers (
            id SERIAL PRIMARY KEY,
            question VARCHAR(255),
            user_answer INTEGER,
            correct_answer FLOAT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


create_quiz_answers_table()
# Route to display the initial question


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', books=books)

# Route to handle book creation


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO books (title, author, pages_num, review)'
                    'VALUES (%s, %s, %s, %s)',
                    (title, author, pages_num, review))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

# Route to display quiz answers


@app.route('/show_answers')
def show_answers():
    return render_template('show_answers.html', name=user_name, correct=correct_answers, wrong=wrong_answers)

# Route to handle quiz


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

            # Connect to the database
            conn = get_db_connection()
            cur = conn.cursor()

            # Insert the user's answer into the database
            cur.execute('INSERT INTO quiz_answers (question, user_answer, correct_answer) VALUES (%s, %s, %s)',
                        (current_question[0], user_answer, current_question[2]))
            conn.commit()

            # Close database connection
            cur.close()
            conn.close()

        current_question = generate_question()
    return render_template('quiz.html', question=current_question)


if __name__ == '__main__':
    app.run(debug=True)
