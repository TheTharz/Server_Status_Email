import smtplib
import psutil
import geocoder
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Email configuration
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))
smtp_user = os.getenv('SMTP_USER')
smtp_password = os.getenv('SMTP_PASSWORD')
to_email = os.getenv('TO_EMAIL')

# Set up logging
logging.basicConfig(
    filename='system_info.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_system_info():
    try:
        # RAM usage
        ram = psutil.virtual_memory()
        ram_usage = f"RAM Usage: {ram.percent}%"

        # Battery level
        battery = psutil.sensors_battery()
        battery_level = f"Battery Level: {battery.percent}%" if battery else "Battery Level: Not available"

        # Memory usage
        memory = psutil.virtual_memory()
        memory_usage = f"Memory Usage: {memory.percent}%"

        # Device location
        location = geocoder.ip('me')
        location_info = f"Location: {location.latlng}" if location.ok else "Location: Not available"

        logging.info("Successfully retrieved system information.")
        return f"{ram_usage}\n{battery_level}\n{memory_usage}\n{location_info}"
    except Exception as e:
        logging.error(f"Error retrieving system information: {str(e)}")
        return "Failed to retrieve system information."

def send_email():
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = 'Automated System Information'

    body = f"This is an automated email sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n\n"
    body += get_system_info()
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_user, to_email, text)
        server.quit()
        logging.info(f"Email sent successfully to {to_email}")
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")

if __name__ == "__main__":
    sri_lanka_tz = pytz.timezone('Asia/Colombo')
    current_time = datetime.now(sri_lanka_tz)

    if current_time.hour == 6 or current_time.hour == 18:
        send_email()
    else:
        logging.info(f"Current time is {current_time.hour}:{current_time.minute}. Script runs only at 6 AM or 6 PM.")
