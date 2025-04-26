# collector.py

import requests
from bs4 import BeautifulSoup
import json

class WebScraper:
    def __init__(self, websites):
        self.websites = websites

    def fetch_data(self):
        collected_data = []
        for url in self.websites:
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad responses
                data = self.extract_data(response.text, url)
                if data:
                    collected_data.append(data)
            except requests.RequestException as e:
                print(f"Error fetching {url}: {e}")
        return collected_data

    def extract_data(self, html_content, url):
        soup = BeautifulSoup(html_content, 'html.parser')
        # Placeholder for data extraction logic
        project_name = self.get_project_name(soup)
        project_location = self.get_project_location(soup)
        project_type = self.get_project_type(soup)
        contact_name = self.get_contact_name(soup)
        mobile_number = self.get_mobile_number(soup)

        return {
            "Project Name": project_name,
            "Project Location": project_location,
            "Project Type": project_type,
            "Contact Name": contact_name,
            "Mobile Number": mobile_number,
            "Source URL": url
        }

    def get_project_name(self, soup):
        # Logic to extract project name from soup
        return soup.find('h1').text.strip() if soup.find('h1') else None

    def get_project_location(self, soup):
        # Logic to extract project location from soup
        return soup.find('span', class_='location').text.strip() if soup.find('span', class_='location') else None

    def get_project_type(self, soup):
        # Logic to extract project type from soup
        return soup.find('span', class_='type').text.strip() if soup.find('span', class_='type') else None

    def get_contact_name(self, soup):
        # Logic to extract contact name from soup
        return soup.find('span', class_='contact-name').text.strip() if soup.find('span', class_='contact-name') else None

    def get_mobile_number(self, soup):
        # Logic to extract mobile number from soup
        return soup.find('span', class_='mobile-number').text.strip() if soup.find('span', class_='mobile-number') else None

def load_websites_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        # Extract just the URLs from the websites array
        return [website["url"] for website in data.get("websites", [])]
    

def collect_data():
    """Collect data from websites defined in the configuration file."""
    websites = load_websites_from_json('src/config/websites.json')
    scraper = WebScraper(websites)
    return scraper.fetch_data()

if __name__ == "__main__":
    websites = load_websites_from_json('src/config/websites.json')
    scraper = WebScraper(websites)
    data = scraper.fetch_data()
    # Further processing of data can be done here (e.g., cleaning, exporting)