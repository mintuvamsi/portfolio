import configparser
import flask
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import psycopg2
from datetime import datetime
import requests

# Import the library for interacting with ChatGPT
# Import the necessary functions or classes to communicate with ChatGPT

# Initialize Flask app
server = flask.Flask(__name__)

# Initialize Dash app within the Flask app
app = dash.Dash(__name__, server=server)

# Read database configuration from db.INI file
config = configparser.ConfigParser()
config.read('roul_qs/db.INI')

# Function to establish a database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=config['db_connection']['host'],
        database=config['db_connection']['database'],
        user=config['db_connection']['user'],
        password=config['db_connection']['password']
    )
    return conn

# Define Dash layout
app.layout = html.Div([
    html.H1("Correct Answers Count by User"),
    html.Div(id='chat-output', style={'height': '400px', 'overflowY': 'scroll'}),
    dcc.Input(id='user-input', type='text', placeholder='Enter your message...'),
    html.Button('Send', id='send-button', n_clicks=0),
    html.Div(id='chat-assistant-output')
])

# Define callback to handle user input and generate bot response
@app.callback(
    [Output('chat-output', 'children'),
     Output('chat-assistant-output', 'children')],
    [Input('send-button', 'n_clicks')],
    [dash.dependencies.State('user-input', 'value')]
)
def update_chat_output(n_clicks, user_input):
    chat_output = []
    chat_assistant_output = []

    if n_clicks > 0 and user_input:
        # Replace this part with code to communicate with ChatGPT
        # Get response from ChatGPT based on user input
        bot_response = "Placeholder response from ChatGPT"
        # End of code to interact with ChatGPT

        chat_output.append(html.P('You: ' + user_input))
        chat_output.append(html.P('Bot: ' + bot_response))

        if "Correct Answers Count by Date" in bot_response:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT qa.date, COUNT(*) AS correct_answers_count
                FROM public.userquizmapping AS uqm
                JOIN public.quiz_answers AS qa ON uqm.question_id = qa.id
                JOIN public.Users AS u ON uqm.user_id = u.id
                WHERE uqm.correct_answer = qa.correct_answer
                GROUP BY qa.date
                ORDER BY qa.date;
            """)
            rows = cur.fetchall()
            cur.close()
            conn.close()

            dates = [row[0] for row in rows]
            correct_answers_count = [row[1] for row in rows]

            figure = {
                'data': [
                    {'x': dates, 'y': correct_answers_count, 'type': 'line', 'name': 'Correct Answers Count'}
                ],
                'layout': {
                    'title': 'Correct Answers Count by Date',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Correct Answers Count'}
                }
            }
            chat_assistant_output.append(dcc.Graph(id='correct-answers-graph', figure=figure))

    return chat_output, chat_assistant_output


# Initialize ChatGPT client
class ChatGPTClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.openai.com/v1/engines/davinci-codex/completions'

    def send_message(self, message):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        data = {
            'prompt': message,
            'max_tokens': 50  # Adjust as needed
        }
        response = requests.post(self.base_url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json().get('choices')[0]['text']
        else:
            return "Error: Failed to get response from ChatGPT"

# Initialize ChatGPT client with API key
chatgpt_client = ChatGPTClient(api_key='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')

# Define callback to handle user input and generate bot response
@app.callback(
        [Output('chat-output', 'children'),
     Output('chat-assistant-output', 'children')],
    [Input('send-button', 'n_clicks')],
    [dash.dependencies.State('user-input', 'value')])

def update_chat_output(n_clicks, user_input):
    chat_output = []
    chat_assistant_output = []

    if n_clicks > 0 and user_input:
        # Call ChatGPT API to get bot response
        bot_response = chatgpt_client.send_message(user_input)

        chat_output.append(html.P('You: ' + user_input))
        chat_output.append(html.P('Bot: ' + bot_response))

        # Add logic to handle special cases or additional actions based on the bot response

        # Return both chat outputs
        return chat_output, chat_assistant_output

    # If no user input, return empty outputs
    return [], []

# Run the Flask app
if __name__ == '__main__':
    app.run_server(debug=True)
