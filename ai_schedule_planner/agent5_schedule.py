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

# Load course schedule data from CSV file
def load_schedule(filename):
    schedule = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            schedule.append(row)
    return schedule

# Function to send a notification email
def send_learning_notification(course, recipient_email, missed_classes, total_classes):
    sender_email = ""  # Replace with your email
    sender_password = ""  # Replace with your email password
    subject = f"Attendance Reminder for {course}"

    body = f"""\
    Hi there,

    This is a reminder for your {course} class.

    You have missed {missed_classes} out of {total_classes} classes.
    Please make sure to attend your upcoming classes to maintain a good attendance record.

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
        print(f"Notification email sent for {course}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Learning agent: Learn from past attendance and adapt notifications
def learning_agent(schedule, attendance_data, recipient_email):
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Track the total number of classes missed and attended for each course
    for event in schedule:
        course = event['Subject']
        event_date = event['Date']

        # Only send a reminder if it's a class scheduled today
        if event_date == current_date:
            if course in attendance_data:
                total_classes = attendance_data[course]['total_classes']
                attended_classes = attendance_data[course]['attended_classes']
                missed_classes = total_classes - attended_classes

                # Send a reminder if the student has missed more than 2 classes
                if missed_classes > 2:
                    send_learning_notification(course, recipient_email, missed_classes, total_classes)
                else:
                    print(f"Good attendance for {course} — {attended_classes}/{total_classes} classes attended.")
            else:
                print(f"No attendance data for {course}.")

# Load attendance and schedule data from CSV files and test the agent
recipient_email = ""  # Replace with the student's email
attendance_data = load_attendance('attendance.csv')
schedule = load_schedule('course_schedule.csv')

# Run the learning agent to adapt notifications based on past attendance
learning_agent(schedule, attendance_data, recipient_email)
