import csv
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load schedule from CSV file
def load_schedule(filename):
    schedule = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            schedule.append(row)
    return schedule

# Load holidays from CSV file
def load_holidays(filename):
    holidays = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            holidays.append(row)
    return holidays

# Function to check if today is a holiday
def is_holiday(holidays):
    today_date = datetime.now().strftime("%Y-%m-%d")
    today_day = datetime.now().strftime("%A")

    for holiday in holidays:
        if holiday['Date'] == today_date or holiday['Day'] == today_day:
            print(f"Today is a holiday: {holiday['Reason']}. No class notifications will be sent.")
            return True
    return False

# Function to send an email reminder
def send_email_reminder(course, location, time, recipient_email):
    sender_email = ""  # Replace with your email
    sender_password = ""  # Replace with your email password
    subject = f"Upcoming Class Reminder: {course}"

    body = f"""\
    Hi there,

    This is a reminder that you have an upcoming class:

    Course: {course}
    Time: {time}
    Location: {location}

    Please make sure to attend.

    Best regards,
    AIPlannerReminder
    """

    # Create the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print(f"Email reminder sent for {course} at {time}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Email-based reminder agent
def email_reminder_agent(schedule, holidays, recipient_email):
    # Check if today is a holiday
    if is_holiday(holidays):
        return  # Skip notifications if today is a holiday

    current_day = datetime.now().strftime("%A")
    current_time = datetime.now()

    for event in schedule:
        # Extract the event time and calculate the notification time
        event_time_str = event['Time'].split('-')[0]  # Only the start time
        event_time = datetime.strptime(event_time_str, "%H:%M").replace(
            year=current_time.year, month=current_time.month, day=current_time.day
        )

        # Calculate 15 minutes before class start time
        notification_time = event_time - timedelta(minutes=15)

        # Check if it's the correct day and within 15 minutes of the class
        if event['Day'] == current_day and current_time >= notification_time and current_time < event_time:
            send_email_reminder(event['Course'], event['Location'], event['Time'], recipient_email)
            break  # Send one notification and stop further checking
    else:
        print("No upcoming classes within the next 15 minutes.")

# Load schedule and holidays data from CSV files and test the agent
recipient_email = ""  # Replace with the student's email
schedule = load_schedule('courses.csv')
holidays = load_holidays('holidays.csv')
email_reminder_agent(schedule, holidays, recipient_email)
