import pandas as pd
import re

# Your DataFrame
data = {
    'Text': [
        'Tue 20 Feb 24', 'Wed 21 Feb 24', 'Thu 22 Feb 24', 'Fri 23 Feb 24',
        'Sat 24 Feb 24', 'Sun 25 Feb 24', 'Mon 26 Feb 24', 'Tue 27 Feb 24',
        'Wed 28 Feb 24', 'Thu 29 Feb 24', 'Fri 01 Mar 24', '14-22', 'Off',
        'Off', '21-05', '18-02', '18-02', '12-20', 'Off', 'Off', '22-06',
        '18-02', '(HOL-Paid 14:00-22:00)'
    ]
}
df = pd.DataFrame(data)

# Regular expressions for date and time
date_pattern = r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s\d{2}\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2}'
time_pattern = r'\b\d{2}:\d{2}\b'

# Function to extract date and time
def extract_date(text):
    date_match = re.search(date_pattern, text)
    return date_match.group(0) if date_match else None

def extract_time(text):
    time_match = re.search(time_pattern, text)
    return time_match.group(0) if time_match else None

# Extracting date and time
df['Date'] = df['Text'].apply(extract_date)
df['Time'] = df['Text'].apply(extract_time)
print(df)

# Assigning values from rows 11 to 22 to the 'Time' column
df['Time'] = df['Time'].fillna(df['Text'].iloc[11:23].values)

# Dropping rows 11 to 22
df = df.drop(df.index[11:23])

# Resetting index
df.reset_index(drop=True, inplace=True)

# Displaying the modified DataFrame
print(df)
