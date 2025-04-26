# main.py

import schedule
import time
from scraper.collector import collect_data
from data.cleaner import clean_data
from data.exporter import export_to_excel
from utils.email_sender import send_email
from utils.scheduler import setup_scheduler
from config.settings import EMAIL_CONFIG

def main():
    # Step 1: Collect data from websites
    raw_data = collect_data()

    # Step 2: Clean and organize the data
    cleaned_data = clean_data(raw_data)

    # Step 3: Export the cleaned data to an Excel file
    excel_file_path = export_to_excel(cleaned_data)

    # Step 4: Send the Excel file via email
    send_email(EMAIL_CONFIG['recipient'], excel_file_path)  # Updated to access the recipient key

def run_scheduler():
    # Schedule the main function to run at specified intervals
    setup_scheduler(main)

if __name__ == "__main__":
    # Run the main function immediately once
    print("Running scraper immediately...")
    main()
    
    # Then setup and run the scheduler
    print("Setting up scheduler for future runs...")
    run_scheduler()
    while True:
        schedule.run_pending()
        time.sleep(1)