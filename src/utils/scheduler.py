import schedule
import logging
from config.settings import SCHEDULING_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_scheduler(func):
    """
    Setup a scheduler to run the specified function at configured intervals.
    
    Parameters:
    func (function): The function to be scheduled.
    """
    interval_minutes = SCHEDULING_CONFIG.get('interval_minutes', 60)
    start_time = SCHEDULING_CONFIG.get('start_time', '08:00')
    
    logging.info(f"Setting up scheduler to run every {interval_minutes} minutes, starting at {start_time}")
    
    # Schedule the job at the specified time
    schedule.every().day.at(start_time).do(func)
    
    # Also schedule to run every X minutes
    schedule.every(interval_minutes).minutes.do(func)
    
    logging.info("Scheduler setup complete")