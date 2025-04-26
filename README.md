# Web Scraper Tool

## Overview

The Web Scraper Tool is an automated application designed to visit a predefined list of websites, collect specific data, and save it into an Excel (XLS) file. The tool is capable of handling different website structures and organizes the collected data into a structured format. It also includes features for scheduling regular scraping sessions and sending email notifications with the results.

## Features

- **Data Collection**: Automatically visits specified websites and extracts relevant information including project names, locations, types, and contact details.
- **Intelligent Parsing**: Uses specialized parsers for different website types (e.g., GitHub, portfolios) and falls back to generic parsing for unknown sites.
- **Data Cleaning**: Cleans and organizes the collected data to ensure accuracy and consistency.
- **Excel Export**: Saves the cleaned data into an Excel file with proper formatting, including color-coding for data quality.
- **Email Notification**: Sends the final Excel file via email to specified recipients.
- **Scheduled Automation**: Runs the scraping process at configured intervals using a flexible scheduler.
- **Fallback Mechanisms**: Uses metadata when live extraction fails to ensure data continuity.
- **Detailed Logging**: Maintains comprehensive logs of all operations for debugging and monitoring.

## Project Structure

```bash
web-scraper-tool/
├── collected_data/           # Output directory for generated Excel files
├── logs/                     # Directory for log files
├── src/                      # Source code directory
│   ├── main.py               # Entry point for the application
│   ├── scraper/              # Modules for web scraping functionality
│   │   ├── __init__.py
│   │   ├── collector.py      # Handles data collection from websites
│   │   └── parser.py         # Parses raw data to extract specific information
│   ├── data/                 # Modules for data processing
│   │   ├── __init__.py
│   │   ├── cleaner.py        # Cleans and organizes the extracted data
│   │   └── exporter.py       # Exports cleaned data to Excel files
│   ├── utils/                # Utility modules
│   │   ├── __init__.py
│   │   ├── email_sender.py   # Manages email sending functionality
│   │   └── scheduler.py      # Automates the scraping process
│   └── config/               # Configuration files
│       ├── __init__.py
│       ├── settings.py       # Configuration settings for the application
│       └── websites.json     # Predefined list of websites to scrape
├── requirements.txt          # Lists project dependencies
├── .gitignore                # Specifies files to ignore in version control
└── README.md                 # Documentation for the project
```

## How It Works

The Web Scraper Tool operates through the following workflow:

1. **Configuration**:
   - The tool reads configuration from `settings.py` for email, scheduling, Excel export, and logging settings.
   - Website targets are loaded from `websites.json` which contains URLs and metadata for each site.

2. **Data Collection**:
   - The `collector.py` module visits each configured website and extracts raw HTML content.
   - It handles HTTP requests, retries for failed connections, and uses proper headers to mimic normal browser behavior.
   - If a website can't be accessed, it falls back to using metadata from the configuration.

3. **Data Parsing**:
   - The `parser.py` module processes the raw HTML to extract structured information.
   - It uses specialized parsers for known websites (GitHub, Sudancar, portfolio sites) and a generic parser for others.
   - Extracted data includes project names, locations, types, contact names, and mobile numbers.

4. **Data Cleaning**:
   - The `cleaner.py` module processes the extracted data to ensure quality and consistency.
   - It standardizes formats, removes duplicates, handles missing values, and formats phone numbers consistently.
   - A data quality score is assigned to each entry to indicate completeness and reliability.

5. **Data Export**:
   - The `exporter.py` module generates a formatted Excel file with the cleaned data.
   - It applies proper styling with color-coding based on data quality and extraction status.
   - New data is appended to existing files with timestamps rather than overwriting previous results.

6. **Email Notification**:
   - The `email_sender.py` module sends the generated Excel file via email to specified recipients.
   - It includes a customizable subject and body message with details about the data collection.

7. **Scheduling**:
   - The `scheduler.py` module manages automated execution at configured intervals.
   - It supports both time-based scheduling (e.g., daily at 8:00 AM) and interval-based scheduling (e.g., every hour).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/web-scraper-tool.git
   ```

2. Navigate to the project directory:

   ```bash
   cd web-scraper-tool
   ```

3. Create and activate a virtual environment (recommended):

   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create required directories if they don't exist:

   ```bash
   mkdir -p collected_data logs
   ```

## Configuration

### Email Settings

Edit `src/config/settings.py` to configure email settings:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # Your SMTP server
    'smtp_port': 587,                 # SMTP port
    'username': 'your-email@gmail.com',  # Your email address
    'password': 'your-app-password',     # Your email password or app password
    'recipient': 'recipient@example.com' # Default recipient email
}
```

For Gmail, you'll need to generate an App Password if you have 2-factor authentication enabled.

### Scheduling Settings

Configure how often the scraper runs:

```python
SCHEDULING_CONFIG = {
    'interval_minutes': 60,     # Run every 60 minutes
    'start_time': '08:00',      # First run of the day at 8:00 AM
    'run_on_weekends': True     # Set to False to skip weekends
}
```

### Output Settings

Configure the Excel output:

```python
EXCEL_CONFIG = {
    'output_file': 'scraped_data.xlsx',  # Output filename
    'sheet_name': 'Projects',            # Sheet name
    'output_dir': 'collected_data'       # Output directory
}
```

### Website Targets

Edit `src/config/websites.json` to add or modify the websites to scrape:

```json
{
  "websites": [
    {
      "name": "Example Site",
      "url": "https://www.example.com",
      "metadata": {
        "type": "Example Type",
        "location": "Example Location",
        "contact_name": "John Doe",
        "mobile_number": "+1-234-567-8901"
      }
    },
    // Add more websites here
  ]
}
```

The metadata is used as fallback information if the website cannot be accessed or data cannot be extracted.

## Usage

### Running Manually

To run the scraper once:

```bash
python src/main.py
```

This will:

1. Execute the scraping process immediately
2. Generate an Excel file in the `collected_data` directory
3. Send the file via email if configured
4. Then start the scheduler for subsequent runs

### Running as a Scheduled Task

The scheduler starts automatically when you run `main.py`. To run only the scheduler without an immediate execution:

```bash
python -c "from src.utils.scheduler import setup_scheduler; from src.main import main; import schedule, time; setup_scheduler(main); print('Scheduler started.'); while True: schedule.run_pending(); time.sleep(1)"
```

### Output Files

After running the scraper:

1. **Excel Reports**: Located in the `collected_data` directory
2. **Log Files**: Located in the `logs` directory with date-based filenames

## Troubleshooting

### Common Issues

1. **Email Sending Fails**:
   - Check your SMTP settings in `settings.py`
   - For Gmail, ensure you're using an App Password if 2FA is enabled
   - Verify that your email provider allows SMTP access

2. **No Data Collected**:
   - Check connectivity to the target websites
   - Review the log files for specific error messages
   - Verify that the website structure hasn't changed, which might break the parsers

3. **Scheduler Issues**:
   - Make sure the system time is correct
   - Check the log files for scheduler-related messages
   - Ensure the process is not being terminated by the operating system

### Log Files

Log files are stored in the `logs` directory with filenames based on the date:

```bash
logs/scraper_20230501.log
```

Check these logs for detailed information about the scraper's operation and any errors that occurred.

## Customization

### Adding Custom Parsers

To add support for new websites with specific structures:

1. Edit `src/scraper/parser.py`
2. Add a new specialized parsing function
3. Update the main parsing logic to use your new parser for specific domains

### Extending Data Fields

To collect additional data points:

1. Modify the parsing functions in `parser.py` to extract new data
2. Update the data structures and cleanup logic in `cleaner.py`
3. Modify the Excel export in `exporter.py` to include the new fields

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the LICENSE file for more details
