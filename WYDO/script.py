import pandas as pd
from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta

# Given DataFrame
df = pd.DataFrame({
    'Date': [
        'Tue 20 Feb 24', 'Wed 21 Feb 24', 'Thu 22 Feb 24', 'Fri 23 Feb 24', 'Sat 24 Feb 24',
        'Sun 25 Feb 24', 'Mon 26 Feb 24', 'Tue 27 Feb 24', 'Wed 28 Feb 24', 'Thu 29 Feb 24',
        'Fri 01 Mar 24'
    ],
    'Time': [
        'HOL', 'Off', 'Off', '21:05', '18:02', '18:02', '14:22', 'Off', 'Off', '22:06', '18:02'
    ]
})

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%a %d %b %y')

# Convert 'Time' column to datetime format
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M', errors='coerce').dt.time

# Filter out rows with invalid time values (NaT)
df = df.dropna(subset=['Time'])

# Create a Calendar object
cal = Calendar()

# Default alert settings (10 minutes before the event)
default_alert = timedelta(hours=-3)

# Default sound file URL
default_sound_url = 'https://example.com/alert_sound.mp3'

# Add events to the calendar
for index, row in df.iterrows():
    event = Event()
    event.add('summary', 'Event')
    # Subtract 3 hours from the event time to set the alarm
    alarm_time = datetime.combine(row['Date'], row['Time']) + default_alert
    event.add('dtstart', datetime.combine(row['Date'], row['Time']))
    event.add('dtend', datetime.combine(row['Date'], row['Time']))
    # Add VALARM component with default alert
    alarm = Alarm()
    alarm.add('action', 'AUDIO')
    alarm.add('trigger', default_alert)
    # Set alarm sound URL
    alarm.add('attach', default_sound_url)
    event.add_component(alarm)
    cal.add_component(event)

# Save the calendar to a file
with open('calendar_with_alarm.ics', 'wb') as f:
    f.write(cal.to_ical())
