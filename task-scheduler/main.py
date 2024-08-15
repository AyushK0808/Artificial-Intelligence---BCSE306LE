import comtypes.client
import time
from datetime import datetime, timedelta
import threading

def open_ppt(file_path):
    # Open PowerPoint application
    ppt_app = comtypes.client.CreateObject("PowerPoint.Application")
    ppt_app.Visible = 1  # Make PowerPoint application visible
    presentation = ppt_app.Presentations.Open(file_path)
    presentation.SlideShowSettings.Run()
    return ppt_app, presentation

def close_ppt(ppt_app, presentation):
    # Close the presentation and PowerPoint application
    presentation.Close()
    ppt_app.Quit()

def schedule_ppt(file_path, start_time, duration):
    start_delay = (start_time - datetime.now()).total_seconds()
    end_time = start_time + timedelta(minutes=duration)
    end_delay = (end_time - datetime.now()).total_seconds()

    # Wait until the start time
    if start_delay > 0:
        time.sleep(start_delay)
    
    # Open the PowerPoint presentation
    ppt_app, presentation = open_ppt(file_path)

    # Wait for the duration
    if end_delay > 0:
        time.sleep(end_delay)

    # Close the PowerPoint presentation
    close_ppt(ppt_app, presentation)

# File path to the PowerPoint file
file_path = "C:/Users/theof/OneDrive/Desktop/real_isro.pptx"

# Schedule times
start_time = datetime(2024, 7, 26, 1, 15, 0)  # Set the start time
duration = 2  # Duration in minutes

# Run the scheduler in a separate thread
scheduler_thread = threading.Thread(target=schedule_ppt, args=(file_path, start_time, duration))
scheduler_thread.start()
