import csv
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Load attendance data from CSV file
def load_attendance(filename):
    attendance_data = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            course = row['Course']
            attended = row['Attended'] == 'Yes'  # Convert 'Yes'/'No' to True/False
            if course not in attendance_data:
                attendance_data[course] = {'total_classes': 0, 'attended_classes': 0}
            attendance_data[course]['total_classes'] += 1
            if attended:
                attendance_data[course]['attended_classes'] += 1
    return attendance_data

# Function to calculate attendance percentage
def calculate_attendance_percentage(attendance_data):
    attendance_percentage = {}
    for course, data in attendance_data.items():
        total = data['total_classes']
        attended = data['attended_classes']
        attendance_percentage[course] = (attended / total) * 100 if total > 0 else 0
    return attendance_percentage

# Function to send a notification email
def send_attendance_notification(course, attendance_percentage, recipient_email):
    sender_email = ""  # Replace with your email
    sender_password = ""  # Replace with your email password
    subject = f"Attendance Alert for {course}"

    body = f"""\
    Hi there,

    Your attendance for {course} is currently at {attendance_percentage:.2f}%, which is below the required 75%.
    Please make sure to attend your upcoming classes to maintain the required attendance rate.

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
        print(f"Attendance alert email sent for {course}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Goal-based attendance agent
def attendance_goal_agent(attendance_data, recipient_email):
    # Calculate attendance percentages for each course
    attendance_percentage = calculate_attendance_percentage(attendance_data)

    # Check if any course's attendance is below 75% and send a notification
    for course, percentage in attendance_percentage.items():
        if percentage < 75:
            send_attendance_notification(course, percentage, recipient_email)
        else:
            print(f"Attendance for {course} is satisfactory at {percentage:.2f}%.")

# Load attendance data and run the goal-based attendance agent
recipient_email = ""  # Replace with the student's email
attendance_data = load_attendance('attendance.csv')
attendance_goal_agent(attendance_data, recipient_email)
