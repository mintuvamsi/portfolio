import cv2
import numpy as np
import pandas as pd
import pytesseract

# Set the path to the Tesseract executable (update this path based on your installation)
pytesseract.pytesseract.tesseract_cmd = '/Users/vamsi/anaconda3/envs/wydo/bin/tesseract'

# Read in the image
img = cv2.imread('IMG_1472.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

# Apply edge detection to the grayscale image
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Use the Hough transform to find lines in the edge image
lines = cv2.HoughLines(edges, rho=1, theta=np.pi/180, threshold=100)

# Create a list to store the line information
line_list = []

# Iterate over the lines and draw them on the image
for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    line_list.append({'rho': rho, 'theta': theta, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})

# Create a pandas DataFrame from the line list
df = pd.DataFrame(line_list)

# Create a binary image with white pixels at the locations of the lines
mask = np.zeros_like(edges)
for _, row in df.iterrows():
    rho = row['rho']
    theta = row['theta']
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(mask, (x1, y1), (x2, y2), (255, 255, 255), 2)

# Combine the binary image with the original image to show only the lines
scanned_img = cv2.bitwise_and(img, img, mask=mask)

# Convert the scanned image to grayscale for text extraction
scanned_gray = cv2.cvtColor(scanned_img, cv2.COLOR_BGR2GRAY)

# Use Tesseract OCR to extract text
text = pytesseract.image_to_string(scanned_gray)

# Display the DataFrame
print("Line Information:")
print(df)
print("\nText Extracted:")
print(text)


import cv2
import pytesseract
import pandas as pd

# Set the path to the Tesseract executable (update this path based on your installation)
pytesseract.pytesseract.tesseract_cmd = '/Users/vamsi/anaconda3/envs/wydo/bin/tesseract'

def ocr_to_dataframe(image_path):
    # Read the image using OpenCV
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use Tesseract to perform OCR on the grayscale image
    text = pytesseract.image_to_string(gray)

    # Split the text into lines
    lines = text.split('\n')

    # Create a DataFrame from the lines
    df = pd.DataFrame({'Text': lines})

    return df

# Replace 'your_image_path.jpg' with the path to your image
image_path = '/Users/vamsi/Project_ai/WYDO/IMG_1472.jpg'
result_df = ocr_to_dataframe(image_path)

# Display the resulting DataFrame
print(result_df)

df = pd.DataFrame(result_df)

type(df['Text'].loc[1])

df = df[df.applymap(lambda x: x != '').sum(axis=1) > 0]
df.reset_index(inplace=True, drop=True)

import re 

# Assuming the data is in Column 0

# Regular expression to find date format
date_pattern = re.compile(r'^[a-zA-Z]+\s\d{2}\s[a-zA-Z]+\s\d{2}$')

# Function to check if a row matches the date format
def is_date(row):
    return bool(date_pattern.match(row))

# Apply the function to create a boolean mask
date_mask = df['Text'].apply(is_date)


df2 = pd.DataFrame()
# Create a new column for date information
df2['Date_Info'] = df['Text'].where(date_mask)
df2

df3 = pd.DataFrame()
# Create another column for the rest of the information
df3['Other_Info'] = df['Text'].where(~date_mask)
df3.dropna(inplace=True)
df3.reset_index(inplace=True)


df2.dropna(inplace=True)

# Concatenate DataFrames vertically
merged_df = pd.concat([df2, df3], axis=1, ignore_index=True)

# Display the merged DataFrame
print(merged_df)

merged_df.dropna(inplace=True)


merged_df.rename(columns={0: 'Date', 2: 'Time'}, inplace=True)

merged_df.drop(columns=1, inplace=True)

def replace_time_with_colon(time_str):
    if time_str == 'Off':
        return 'Off'
    else:
        return ':'.join(time_str.split('-'))


merged_df.Time = merged_df.Time.apply(replace_time_with_colon)


merged_df.Date = pd.to_datetime(merged_df.Date)

# Function to convert time strings to time format
def convert_to_time(time_str):
    if time_str == 'Off':
        return pd.NaT  # Represents a missing/undefined value for time
    else:
        return pd.to_datetime(time_str, format='%H:%M').time()

# Apply the function to the "Time" column
merged_df['Time'] = merged_df['Time'].apply(convert_to_time)

# Print the updated DataFrame
print(merged_df)

# Function to convert time strings to datetime
def convert_to_datetime(date_str, time_str):
    if time_str == 'Off':
        return None
    else:
        return datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')

# Function to calculate alarm times
def calculate_alarm_time(row):
    datetime_obj = convert_to_datetime(row['Date'], row['Time'])
    if datetime_obj is not None and datetime_obj > datetime.now():
        return datetime_obj - timedelta(hours=3)
    else:
        return None

# Create a new column 'AlarmTime' in the DataFrame
merged_df['AlarmTime'] = merged_df.apply(calculate_alarm_time, axis=1)

# Function to create reminder using osascript
def create_reminder(title, date_time):
    script = f'do shell script "echo \'{title}\' | pbcopy && open -a Reminders && sleep {date_time.timestamp() - datetime.now().timestamp()}"'
    subprocess.run(['osascript', '-e', script])

# Create reminders
for index, row in merged_df.iterrows():
    if row['AlarmTime'] is not None:
        title = f"Alarm for {row['Date']} at {row['Time']}"
        create_reminder(title, row['AlarmTime'])

# Function to calculate alarm times
def calculate_alarm_time(row):
    datetime_obj = convert_to_datetime(row['Date'], row['Time'])
    if datetime_obj is not None and datetime_obj > datetime.now():
        return datetime_obj - timedelta(hours=3)
    else:
        return None

# Create a new column 'AlarmTime' in the DataFrame
df['AlarmTime'] = df.apply(calculate_alarm_time, axis=1)

# Function to create reminder using osascript
def create_reminder(title, date_time):
    script = f'do shell script "echo \'{title}\' | pbcopy && open -a Reminders && sleep {date_time.timestamp() - datetime.now().timestamp()}"'
    subprocess.run(['osascript', '-e', script])

# Create reminders
for index, row in df.iterrows():
    if row['AlarmTime'] is not None:
        title = f"Alarm for {row['Date']} at {row['Time']}"
        create_reminder(title, row['AlarmTime'])
