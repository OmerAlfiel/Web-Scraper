"""
Settings Configuration

Configuration settings for the web scraper tool.
These settings can be customized to control the behavior of the application.
"""

import os
from datetime import datetime

# Try to load environment variables if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Email configuration
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', 587)),
    'username': os.getenv('EMAIL_USERNAME', ''),
    'password': os.getenv('EMAIL_PASSWORD', ''),  # IMPORTANT: Use app password!
    'recipient': os.getenv('EMAIL_RECIPIENT', '')
}

# Scheduling configuration
SCHEDULING_CONFIG = {
    'interval_minutes': int(os.getenv('SCHEDULE_INTERVAL', 60)),  # Interval to run the scraper in minutes
    'start_time': os.getenv('SCHEDULE_START_TIME', '08:00'),      # Time to start the scraper (24-hour format)
    'run_on_weekends': os.getenv('SCHEDULE_RUN_WEEKENDS', 'True').lower() == 'true'
}

# Excel file configuration
EXCEL_CONFIG = {
    'output_file': os.getenv('EXCEL_OUTPUT_FILE', 'scraped_data.xlsx'),  # Name of the output Excel file
    'sheet_name': os.getenv('EXCEL_SHEET_NAME', 'Projects'),             # Name of the sheet in the Excel file
    'use_timestamp': os.getenv('EXCEL_USE_TIMESTAMP', 'False').lower() == 'true',  # Add timestamp to filename
    'output_dir': os.getenv('EXCEL_OUTPUT_DIR', 'data')                  # Directory to save Excel files
}

# Logging configuration
LOGGING_CONFIG = {
    'log_file': os.getenv('LOG_FILE', os.path.join('logs', f'scraper_{datetime.now().strftime("%Y%m%d")}.log')),
    'log_level': os.getenv('LOG_LEVEL', 'DEBUG')                          # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
}

# Other configurations
OTHER_CONFIG = {
    'max_retries': int(os.getenv('MAX_RETRIES', 3)),             # Maximum number of retries for failed requests
    'timeout': int(os.getenv('REQUEST_TIMEOUT', 10)),            # Timeout for HTTP requests in seconds
    'user_agent': os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
}