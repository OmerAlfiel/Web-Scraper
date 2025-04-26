"""
Email Sender Module

This module handles sending emails with attachments.
"""

import os
import logging
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config.settings import EMAIL_CONFIG
from datetime import datetime


def send_email(recipient, attachment_path=None, subject=None, body=None):
    """
    Sends an email with an optional Excel file attachment.
    
    Parameters:
    recipient (str): The email address of the recipient.
    attachment_path (str, optional): The path to the file to be attached.
    subject (str, optional): The email subject. If not provided, a default is used.
    body (str, optional): The email body. If not provided, a default is used.
    
    Returns:
    bool: True if email was sent successfully, False otherwise.
    """
    try:
        # Default subject and body if not provided
        if not subject:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            subject = f"Web Scraper Report - {timestamp}"
        
        if not body:
            body = "Please find attached the latest web scraper report."
            if attachment_path:
                body += f"\n\nFile: {os.path.basename(attachment_path)}"
            body += "\n\nThis is an automated message from the Web Scraper Tool."
        
        # Get email configuration
        smtp_server = EMAIL_CONFIG.get('smtp_server')
        smtp_port = EMAIL_CONFIG.get('smtp_port')
        username = EMAIL_CONFIG.get('username')
        password = EMAIL_CONFIG.get('password')
        
        if not all([smtp_server, smtp_port, username, password]):
            logging.error("Incomplete email configuration")
            return False
        
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Attach the body
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach the file if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                filename = os.path.basename(attachment_path)
                part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(part)
                logging.info(f"Attached file: {filename}")
        elif attachment_path:
            logging.warning(f"Attachment file not found: {attachment_path}")
        
        # Create SMTP session and send the email
        with SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable security
            server.login(username, password)  # Login
            server.send_message(msg)  # Send the email
        
        logging.info(f"Email sent successfully to {recipient}")
        return True
    
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return False


def send_notification(message, subject="Web Scraper Notification"):
    """
    Sends a simple notification email without attachments.
    
    Parameters:
    message (str): The notification message.
    subject (str, optional): The email subject.
    
    Returns:
    bool: True if notification was sent successfully, False otherwise.
    """
    recipient = EMAIL_CONFIG.get('recipient')
    return send_email(recipient, subject=subject, body=message)


def send_error_report(error_message, error_details=None):
    """
    Sends an error report email.
    
    Parameters:
    error_message (str): The main error message.
    error_details (str, optional): Additional error details.
    
    Returns:
    bool: True if error report was sent successfully, False otherwise.
    """
    subject = "Web Scraper Error Report"
    body = f"The Web Scraper encountered an error:\n\n{error_message}"
    
    if error_details:
        body += f"\n\nError Details:\n{error_details}"
    
    body += "\n\nPlease check the application logs for more information."
    
    recipient = EMAIL_CONFIG.get('recipient')
    return send_email(recipient, subject=subject, body=body)


if __name__ == "__main__":
    # Configure basic logging for testing
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Test sending a notification
    logging.info("Testing email notification...")
    success = send_notification("This is a test notification from the Web Scraper Tool.")
    
    if success:
        logging.info("Test notification sent successfully")
    else:
        logging.error("Failed to send test notification")