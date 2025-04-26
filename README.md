# Web Scraper Tool

## Overview
The Web Scraper Tool is an automated application designed to visit a predefined list of websites, collect specific data, and save it into an Excel (XLS) file. The tool is capable of handling different website structures and organizes the collected data into a structured format.

## Features

- **Data Collection**: Automatically visits specified websites and extracts relevant information.
- **Data Cleaning**: Cleans and organizes the collected data to ensure accuracy and relevance.
- **Excel Export**: Saves the cleaned data into an Excel file with clearly defined columns.
- **Email Notification**: Sends the final Excel file via email or saves it to a specified location.
- **Automation**: Runs the scraping process at scheduled intervals.

## Project Structure

```
web-scraper-tool
├── src
│   ├── main.py               # Entry point for the application
│   ├── scraper
│   │   ├── __init__.py       # Package initialization
│   │   ├── collector.py       # Handles data collection from websites
│   │   └── parser.py         # Parses raw data to extract specific information
│   ├── data
│   │   ├── __init__.py       # Package initialization
│   │   ├── cleaner.py        # Cleans and organizes the extracted data
│   │   └── exporter.py       # Exports cleaned data to an Excel file
│   ├── utils
│   │   ├── __init__.py       # Package initialization
│   │   ├── email_sender.py    # Manages email sending functionality
│   │   └── scheduler.py      # Automates the scraping process
│   └── config
│       ├── __init__.py       # Package initialization
│       ├── settings.py       # Configuration settings for the application
│       └── websites.json     # Predefined list of websites to scrape
├── requirements.txt           # Lists project dependencies
├── .gitignore                 # Specifies files to ignore in version control
└── README.md                  # Documentation for the project
```

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```bash
   cd web-scraper-tool
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Configure the `settings.py` file with your email credentials and scheduling intervals.
2. Update the `websites.json` file with the list of websites you want to scrape.
3. Run the application:

   ```bash
   python src/main.py
   ```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.