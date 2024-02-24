from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
from qs import *
import configparser
from werkzeug.security import generate_password_hash
from datetime import datetime
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

config = configparser.ConfigParser()
config.read('db.INI')

# Function to establish a database connection


def get_db_connection():
    conn = psycopg2.connect(
        host=config['db_connection']['host'],
        database=config['db_connection']['database'],
        user=config['db_connection']['user'],
        password=config['db_connection']['password']
    )
    return conn

# Function to create the quiz_answers table if it doesn't exist


def create_quiz_answers_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        -- Create the table
                CREATE TABLE IF NOT EXISTS quiz_answers (
                id SERIAL PRIMARY KEY,
                question VARCHAR(255),
                user_answer INTEGER,
                correct_answer FLOAT
            );

            -- Add a default date column if it doesn't exist
            ALTER TABLE IF EXISTS quiz_answers
            ADD COLUMN IF NOT EXISTS date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

    """)
    conn.commit()
    cur.close()
    conn.close()
    return "Quiz answers Table Created"


create_quiz_answers_table()

# Route for the login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['username'] = username
            print('working')
            # Redirect to quiz.html upon successful login
            return redirect(url_for('quiz'))  # Redirect to quiz route
        else:
            print('going to login page')
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

# Route for the registration page


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            error = 'Username and password are required'
            return render_template('register.html', error=error)
        if register_user(username, password):
            return redirect(url_for('login'))
        else:
            error = 'Username already exists'
            return render_template('register.html', error=error)
    return render_template('register.html')

# Route for the dashboard page


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

# Route for logging out


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Function to authenticate a user


def authenticate_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if user is not None:  # Check if user exists
        return (user[1], user[2])  # Return username and hashed password
    else:
        return None  # User not found, return None


# Function to register a new user
def register_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cur.fetchone()
    if existing_user:
        cur.close()
        conn.close()
        return False
    else:
        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, hashed_password))
        conn.commit()
        cur.close()
        conn.close()
        return True


# Route to display quiz answers
@app.route('/show_answers')
def show_answers():
    # Ensure user is logged in before showing answers
    if 'username' in session:
        username = session['username']
        return render_template('show_answers.html', username=username, correct=correct_answers, wrong=wrong_answers)
    else:
        # Redirect to login page if user is not logged in
        return redirect(url_for('login'))

# Route to handle quiz


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global current_question, correct_answers, wrong_answers
    if request.method == 'POST':
        user_answer = request.form.get('user_answer')
        date = datetime.now()
        if user_answer is not None and user_answer.isdigit():
            if int(user_answer) == current_question[2]:
                correct_answers += 1
            else:
                wrong_answers += 1

            # Connect to the database
            conn = get_db_connection()
            cur = conn.cursor()

            # Insert the user's answer into the database
            cur.execute('INSERT INTO quiz_answers (question, user_answer, correct_answer, date) VALUES (%s, %s, %s, %s)',
                        (current_question[0], user_answer, current_question[2], date))
            conn.commit()

            # Close database connection
            cur.close()
            conn.close()

        current_question = generate_question()
    return render_template('quiz.html', question=current_question)


if __name__ == '__main__':
    create_quiz_answers_table()
    app.run(debug=True)
