"""
Scheduler Module

This module handles the scheduling of web scraping tasks.
"""

import schedule
import time
import logging
from datetime import datetime, timedelta
from config.settings import SCHEDULING_CONFIG


def setup_scheduler(func):
    """
    Setup a scheduler to run the specified function at configured intervals.
    
    Parameters:
    func (function): The function to be scheduled.
    
    Returns:
    schedule.Job: The scheduled job.
    """
    # Get configuration
    interval_minutes = SCHEDULING_CONFIG.get('interval_minutes', 60)
    start_time = SCHEDULING_CONFIG.get('start_time', '08:00')
    run_on_weekends = SCHEDULING_CONFIG.get('run_on_weekends', True)
    
    logging.info(f"Setting up scheduler to run every {interval_minutes} minutes, starting at {start_time}")
    
    # Create a job wrapper that checks if the job should run
    def job_wrapper():
        now = datetime.now()
        
        # Skip on weekends if configured
        if not run_on_weekends and now.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            logging.info(f"Skipping scheduled run at {now} (weekend)")
            return
        
        # Run the function
        logging.info(f"Running scheduled job at {now}")
        try:
            func()
            logging.info(f"Scheduled job completed at {datetime.now()}")
        except Exception as e:
            logging.error(f"Error in scheduled job: {str(e)}", exc_info=True)
    
    # Schedule daily run at specific time
    daily_job = schedule.every().day.at(start_time).do(job_wrapper)
    
    # Also schedule to run every X minutes
    interval_job = schedule.every(interval_minutes).minutes.do(job_wrapper)
    
    logging.info("Scheduler setup complete")
    return interval_job  # Return the interval job for possible cancellation


def schedule_one_time_job(func, delay_minutes=5):
    """
    Schedule a one-time job to run after a specified delay.
    
    Parameters:
    func (function): The function to be scheduled.
    delay_minutes (int): The delay in minutes before running the job.
    
    Returns:
    schedule.Job: The scheduled job.
    """
    run_time = (datetime.now() + timedelta(minutes=delay_minutes)).strftime("%H:%M:%S")
    logging.info(f"Scheduling one-time job to run at {run_time}")
    
    job = schedule.every().day.at(run_time).do(func)
    
    # Mark the job as one-time
    job.tag('one-time')
    
    # Cancel the job after it runs
    def run_once():
        func()
        schedule.cancel_job(job)
    
    job.job_func = run_once
    
    return job


def run_scheduler_until_complete(timeout_minutes=60):
    """
    Run the scheduler until all jobs are complete or timeout is reached.
    
    Parameters:
    timeout_minutes (int): Maximum time to run in minutes.
    
    Returns:
    bool: True if all jobs completed, False if timeout was reached.
    """
    start_time = time.time()
    timeout_seconds = timeout_minutes * 60
    
    while time.time() - start_time < timeout_seconds:
        # Run pending jobs
        schedule.run_pending()
        
        # Check if there are any pending jobs
        if not any(job.next_run is not None for job in schedule.jobs):
            logging.info("All scheduled jobs completed")
            return True
        
        # Sleep to prevent high CPU usage
        time.sleep(1)
    
    logging.warning(f"Scheduler timed out after {timeout_minutes} minutes")
    return False


def clear_all_jobs():
    """Clear all scheduled jobs."""
    schedule.clear()
    logging.info("All scheduled jobs cleared")


if __name__ == "__main__":
    # Configure basic logging for testing
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Test function
    def test_job():
        logging.info(f"Test job running at {datetime.now()}")
    
    # Test the scheduler
    logging.info("Testing scheduler...")
    setup_scheduler(test_job)
    
    # Run for a short time
    logging.info("Running scheduler for 10 seconds...")
    end_time = time.time() + 10
    try:
        while time.time() < end_time:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Test interrupted by user")
    
    logging.info("Scheduler test complete")