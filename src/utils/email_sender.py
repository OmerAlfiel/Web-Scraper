from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email(recipient, attachment_path):
    """
    Sends an email with the Excel file attachment.
    
    Parameters:
    recipient (str): The email address of the recipient.
    attachment_path (str): The path to the Excel file to be attached.
    """
    from config.settings import EMAIL_CONFIG
    
    # Create email subject and body
    subject = "Web Scraper Report"
    body = "Please find attached the latest web scraper report."
    
    # Email configuration from settings
    from_email = EMAIL_CONFIG['username']
    email_password = EMAIL_CONFIG['password']
    
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = recipient
    msg['Subject'] = subject
    
    # Attach the body
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the file
    if attachment_path:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
            msg.attach(part)
    
    # Create SMTP session
    with SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
        server.starttls()  # Enable security
        server.login(from_email, email_password)  # Login with email and password
        server.send_message(msg)  # Send the email
    
    print(f'Email sent to {recipient} with attachment {attachment_path}')