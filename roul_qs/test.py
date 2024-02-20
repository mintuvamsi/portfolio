import configparser
import psycopg2,random

# Read database configuration from db.INI file
config = configparser.ConfigParser()
config.read('roul_qs/db.INI')

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=config['db_connection']['host'],
        database=config['db_connection']['database'],
        user=config['db_connection']['user'],
        password=config['db_connection']['password']
    )

    # Create a cursor object
    cur = conn.cursor()

    # Fetch records from quiz_answers table
    cur.execute("SELECT id, question, correct_answer, date FROM quiz_answers")
    quiz_answers = cur.fetchall()

    # Fetch user IDs from users table
    cur.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cur.fetchall()]

    # Sync records to UserQuizMapping table
    for quiz_answer in quiz_answers:
        quiz_answer_id, question, correct_answer, date = quiz_answer
        # Randomly select a user ID from the list
        random_user_id = random.choice(user_ids)
        # Insert into UserQuizMapping table
        cur.execute("INSERT INTO UserQuizMapping (user_id, question_id, correct_answer, date) VALUES (%s, %s, %s, %s)",
                    (random_user_id, quiz_answer_id, correct_answer, date))

    # Commit the transaction
    conn.commit()
    print("Syncing completed successfully.")

except psycopg2.Error as e:
    print("Error connecting to PostgreSQL:", e)

finally:
    # Close the cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()
