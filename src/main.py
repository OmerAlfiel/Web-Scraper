"""
Web Scraper Tool - Main Application

This script is the entry point for the web scraping application.
It orchestrates the data collection, cleaning, exporting, and email notification process.
"""

import schedule
import time
import logging
import os
from datetime import datetime
from scraper.collector import collect_data
from data.cleaner import clean_data
from data.exporter import export_to_excel
from utils.email_sender import send_email
from utils.scheduler import setup_scheduler
from config.settings import EMAIL_CONFIG, LOGGING_CONFIG

# Create necessary directories first
os.makedirs('data', exist_ok=True)
os.makedirs('logs', exist_ok=True)
os.makedirs(os.path.dirname(LOGGING_CONFIG['log_file']), exist_ok=True)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG['log_level']),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGGING_CONFIG['log_file']),
        logging.StreamHandler()
    ]
)

def main():
    """Main function that executes the web scraping workflow."""
    start_time = datetime.now()
    logging.info(f"Starting web scraping process at {start_time}")
    
    try:
        # Step 1: Collect data from websites
        logging.info("Collecting data from websites...")
        raw_data = collect_data()
        logging.info(f"Collected data from {len(raw_data)} websites")
        
        if not raw_data:
            logging.warning("No data collected. Exiting process.")
            return
        
        # Step 2: Clean and organize the data
        logging.info("Cleaning and organizing data...")
        cleaned_data = clean_data(raw_data)
        
        # Step 3: Export the cleaned data to an Excel file
        logging.info("Exporting data to Excel...")
        excel_file_path = export_to_excel(cleaned_data)
        
        # Step 4: Send the Excel file via email
        logging.info(f"Sending Excel file to {EMAIL_CONFIG['recipient']}...")
        send_email(EMAIL_CONFIG['recipient'], excel_file_path)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logging.info(f"Web scraping process completed in {duration} seconds")
        
    except Exception as e:
        logging.error(f"Error in web scraping process: {str(e)}", exc_info=True)

def run_scheduler():
    """Setup and run the scheduler for periodic execution."""
    setup_scheduler(main)

if __name__ == "__main__":
    # Run the main function immediately once
    print("Running scraper immediately...")
    main()
    
    # Then setup and run the scheduler
    print("Setting up scheduler for future runs...")
    run_scheduler()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Web scraper stopped by user")
        print("Web scraper stopped. Goodbye!")