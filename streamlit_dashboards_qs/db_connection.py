import psycopg2
from configparser import ConfigParser

def get_db_connection():
    # Read database configuration from .INI file
    config = ConfigParser()
    config.read('db.INI')  # Adjust the file path if necessary
    # Get database connection parameters
    db_params = {
        'host': config['db_connection']['host'],
        'database': config['db_connection']['database'],
        'user': config['db_connection']['user'],
        'password': config['db_connection']['password']
    }

    # Establish database connection
    try:
        connection = psycopg2.connect(**db_params)
        print("Connected to the database.")
        return connection
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

# Test the database connection
if __name__ == "__main__":
    get_db_connection()
