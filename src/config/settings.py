# settings.py

# Configuration settings for the web scraper tool

# Email configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587,
    'username': 'your_email@example.com',
    'password': 'your_password',
    'recipient': 'recipient_email@example.com'
}

# Scheduling configuration
SCHEDULING_CONFIG = {
    'interval_minutes': 60,  # Interval to run the scraper in minutes
    'start_time': '08:00',    # Time to start the scraper (24-hour format)
}

# Excel file configuration
EXCEL_CONFIG = {
    'output_file': 'scraped_data.xlsx',  # Name of the output Excel file
    'sheet_name': 'Projects'               # Name of the sheet in the Excel file
}

# Logging configuration
LOGGING_CONFIG = {
    'log_file': 'scraper.log',  # Log file name
    'log_level': 'INFO'          # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
}

# Other configurations
OTHER_CONFIG = {
    'max_retries': 3,            # Maximum number of retries for failed requests
    'timeout': 10                 # Timeout for HTTP requests in seconds
}