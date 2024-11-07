import csv
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Load course schedule data from CSV file
def load_schedule(filename):
    schedule = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            schedule.append(row)
    return schedule

# Function to send a notification email
def send_important_topic_notification(subject, topic, date, recipient_email):
    sender_email = ""  # Replace with your email
    sender_password = ""  # Replace with your email password
    subject_line = f"Reminder: Important Topic in {subject} on {date}"

    body = f"""\
    Hi there,

    This is a reminder that an important topic will be covered in your {subject} class on {date}:

    Topic: {topic}

    Please make sure to attend and not miss this crucial topic for your learning.

    Best regards,
    AIPlannerReminder
    """

    # Create the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject_line
    message.attach(MIMEText(body, "plain"))

    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print(f"Notification email sent for {subject} on {date}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Utility-based agent
def utility_based_agent(schedule, important_topics, recipient_email):
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Check if today's date matches any important topics in the schedule
    for event in schedule:
        event_date = event['Date']
        subject = event['Subject']
        topic = event['Topic']

        # Send notification if the topic is important and the class is today
        if event_date == current_date and topic in important_topics.get(subject, []):
            send_important_topic_notification(subject, topic, event_date, recipient_email)

# Load course schedule data from CSV and test the agent
recipient_email = ""  # Replace with the student's email
schedule = load_schedule('course_schedule.csv')

# Define important topics for each subject
important_topics = {
    'DBMS': ['Introduction to Databases', 'Normalization', 'SQL Queries', 'Database Security'],
    'Math': ['Calculus', 'Linear Algebra'],
    'Physics': ['Quantum Mechanics', 'Relativity'],
    'English': ["Shakespeare's Hamlet"],
    'Chemistry': ['Chemical Reactions'],
    'AI':['Testing Utility Based Agents']
}

utility_based_agent(schedule, important_topics, recipient_email)
