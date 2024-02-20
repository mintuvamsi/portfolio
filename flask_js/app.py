import configparser
import flask
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import psycopg2
from datetime import datetime

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
    html.Label('Select User:'),
    dcc.Dropdown(
        id='user-dropdown',
        options=[],
        value=None
    ),
    html.Label('Select Correct Answers Count Range:'),
    dcc.RangeSlider(
        id='correct-answers-slider',
        min=0,
        max=100,
        step=1,
        marks={i: str(i) for i in range(0, 101)},
        value=[0, 100]
    ),
    html.Label('Select Date Range:'),
    dcc.DatePickerRange(
        id='date-range-picker',
        start_date_placeholder_text='Start Date',
        end_date_placeholder_text='End Date',
        display_format='YYYY-MM-DD',
        start_date=datetime(2022, 1, 1),
        end_date=datetime.now()
    ),
    dcc.Graph(id='correct-answers-graph'),
    # Dummy input to trigger the callback
    dcc.Input(id='dummy-input', style={'display': 'none'}, value='dummy')
])

# Populate user dropdown options
@app.callback(
    Output('user-dropdown', 'options'),
    [Input('dummy-input', 'value')]
)
def populate_user_dropdown(dummy_input):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM public.Users ORDER BY username")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'label': row[1], 'value': row[0]} for row in rows]

# Define callback to update the graph
@app.callback(
    Output('correct-answers-graph', 'figure'),
    [Input('dummy-input', 'value'),
     Input('user-dropdown', 'value'),
     Input('correct-answers-slider', 'value'),
     Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)

def update_graph(dummy_input, user_id, correct_answers_range, start_date, end_date):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT qa.date, COUNT(*) AS correct_answers_count
        FROM public.userquizmapping AS uqm
        JOIN public.quiz_answers AS qa ON uqm.question_id = qa.id
        JOIN public.Users AS u ON uqm.user_id = u.id
        WHERE uqm.correct_answer = qa.correct_answer
        AND (%s IS NULL OR u.id = %s)
        AND (qa.correct_answer BETWEEN %s AND %s)
        AND (qa.date BETWEEN %s AND %s)
        GROUP BY qa.date
        ORDER BY qa.date;
    """, (user_id, user_id, correct_answers_range[0], correct_answers_range[1], start_date, end_date))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Extract data for plotting
    dates = [row[0] for row in rows]
    correct_answers_count = [row[1] for row in rows]

    # Create a line chart
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

    return figure

# Run the Flask app
if __name__ == '__main__':
    app.run_server(debug=True)
