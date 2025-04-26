# collector.py

"""
Web Scraper Collector Module

This module handles the collection of data from websites.
It includes functionality to fetch web pages and extract relevant information.
"""

import requests
import json
import logging
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from config.settings import OTHER_CONFIG

class WebScraper:
    """Main web scraper class that handles collecting data from websites."""
    
    def __init__(self, websites, selectors=None):
        """
        Initialize the WebScraper.
        
        Args:
            websites (list): List of website URLs to scrape.
            selectors (dict, optional): CSS selectors for different data fields.
        """
        self.websites = websites
        self.selectors = selectors or {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_data(self):
        """
        Fetch data from all configured websites.
        
        Returns:
            list: List of dictionaries containing extracted data.
        """
        collected_data = []
        max_retries = OTHER_CONFIG.get('max_retries', 3)
        timeout = OTHER_CONFIG.get('timeout', 10)
        
        for website in self.websites:
            url = website.get('url')
            metadata = website.get('metadata', {})
            name = website.get('name', url)
            
            logging.info(f"Fetching data from {name} ({url})")
            
            extraction_successful = False
            for attempt in range(max_retries):
                try:
                    response = requests.get(
                        url, 
                        headers=self.headers,
                        timeout=timeout
                    )
                    response.raise_for_status()
                    
                    # Extract data
                    data = self.extract_data(response.text, url, metadata)
                    if data:
                        # Add extraction status field
                        data["Extraction Status"] = "Success - Live Data"
                        collected_data.append(data)
                        logging.info(f"Successfully collected data from {name}")
                        extraction_successful = True
                        break  # Exit retry loop on success
                    else:
                        logging.warning(f"No data extracted from {name}")
                    
                except requests.RequestException as e:
                    logging.error(f"Attempt {attempt+1}/{max_retries} failed for {name}: {str(e)}")
                    if attempt < max_retries - 1:
                        # Wait before retrying (with exponential backoff)
                        time.sleep(2 ** attempt)
            
            # If extraction failed after all retries, use metadata as fallback
            if not extraction_successful:
                logging.warning(f"Using metadata fallback for {name}")
                fallback_data = {
                    "Project Name": metadata.get('name', name),
                    "Project Location": metadata.get('location', 'Unknown'),
                    "Project Type": metadata.get('type', 'Unknown'),
                    "Contact Name": metadata.get('contact_name', 'Unknown'),
                    "Mobile Number": metadata.get('mobile_number', 'Not available'),
                    "Source URL": url,
                    "Extraction Date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Extraction Status": "Failed - Using Metadata Only"
                }
                collected_data.append(fallback_data)
        
        return collected_data
    
    def extract_data(self, html_content, url, metadata=None):
        """
        Extract data from HTML content.
        
        Args:
            html_content (str): HTML content of the webpage.
            url (str): URL of the webpage.
            metadata (dict, optional): Metadata about the website.
            
        Returns:
            dict: Dictionary containing extracted data.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        domain = urlparse(url).netloc
        
        # Try to extract data using custom extraction logic for known domains
        extracted_data = None
        extraction_method = "Generic"
        
        if domain == 'www.sudancar.com':
            extracted_data = self.extract_from_sudancar(soup, url, metadata)
            extraction_method = "Sudancar"
        elif 'github.com' in domain:
            extracted_data = self.extract_from_github(soup, url, metadata)
            extraction_method = "GitHub"
        else:
            # Use generic extraction
            extracted_data = self.extract_generic(soup, url, metadata)
        
        # Add extraction method to data
        if extracted_data:
            extracted_data["Extraction Method"] = extraction_method
        
        return extracted_data
    
    def extract_generic(self, soup, url, metadata=None):
        """
        Generic data extraction method.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content.
            url (str): URL of the webpage.
            metadata (dict, optional): Metadata about the website.
            
        Returns:
            dict: Dictionary containing extracted data.
        """
        # Use the metadata if provided (fallback data)
        metadata = metadata or {}
        
        # Track which fields used metadata fallback
        fallback_fields = []
        
        # Try to extract project name
        project_name = self.get_project_name(soup)
        if not project_name:
            project_name = metadata.get('name')
            if project_name:
                fallback_fields.append("Project Name")
        
        # Other fields with fallback tracking
        project_location = self.get_project_location(soup)
        if not project_location:
            project_location = metadata.get('location')
            if project_location:
                fallback_fields.append("Project Location")
        
        project_type = self.get_project_type(soup)
        if not project_type:
            project_type = metadata.get('type')
            if project_type:
                fallback_fields.append("Project Type")
        
        contact_name = self.get_contact_name(soup)
        if not contact_name:
            contact_name = metadata.get('contact_name')
            if contact_name:
                fallback_fields.append("Contact Name")
        
        mobile_number = self.get_mobile_number(soup)
        if not mobile_number:
            mobile_number = metadata.get('mobile_number')
            if mobile_number:
                fallback_fields.append("Mobile Number")
        
        # Create fallback notes
        fallback_notes = ""
        if fallback_fields:
            fallback_notes = f"Metadata used for: {', '.join(fallback_fields)}"
        
        # Return the extracted data
        return {
            "Project Name": project_name,
            "Project Location": project_location,
            "Project Type": project_type,
            "Contact Name": contact_name,
            "Mobile Number": mobile_number,
            "Source URL": url,
            "Extraction Date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "Fallback Notes": fallback_notes
        }
    
    def extract_from_sudancar(self, soup, url, metadata=None):
        """
        Extract data from Sudancar website.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content.
            url (str): URL of the webpage.
            metadata (dict, optional): Metadata about the website.
            
        Returns:
            dict: Dictionary containing extracted data.
        """
        # Specialized extraction logic for Sudancar
        project_name = soup.find('h1', class_='car-title').text.strip() if soup.find('h1', class_='car-title') else None
        project_location = soup.find('span', class_='location').text.strip() if soup.find('span', class_='location') else None
        project_type = "Automotive"  # Set default type for this domain
        
        # Try to find contact information
        contact_section = soup.find('div', class_='contact-info')
        contact_name = contact_section.find('h3').text.strip() if contact_section and contact_section.find('h3') else None
        mobile_element = soup.find('a', href=lambda href: href and 'tel:' in href)
        mobile_number = mobile_element.text.strip() if mobile_element else None
        
        # Use metadata as fallback
        if metadata:
            project_name = project_name or metadata.get('name')
            project_location = project_location or metadata.get('location')
            project_type = project_type or metadata.get('type')
            contact_name = contact_name or metadata.get('contact_name')
            mobile_number = mobile_number or metadata.get('mobile_number')
        
        return {
            "Project Name": project_name,
            "Project Location": project_location,
            "Project Type": project_type,
            "Contact Name": contact_name,
            "Mobile Number": mobile_number,
            "Source URL": url,
            "Extraction Date": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def extract_from_github(self, soup, url, metadata=None):
        """
        Extract data from GitHub website.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content.
            url (str): URL of the webpage.
            metadata (dict, optional): Metadata about the website.
            
        Returns:
            dict: Dictionary containing extracted data.
        """
        # GitHub profile/repository specific extraction
        project_name = soup.find('h1', class_='').text.strip() if soup.find('h1', class_='') else None
        
        # For GitHub, set some defaults
        project_type = "Software Development"
        project_location = None
        
        # Try to find profile information if it's a profile page
        profile_info = soup.find('div', class_='js-profile-editable-area')
        if profile_info:
            # It's a profile page
            location_element = profile_info.find('span', itemprop='homeLocation')
            project_location = location_element.text.strip() if location_element else None
            
            name_element = profile_info.find('span', itemprop='name')
            contact_name = name_element.text.strip() if name_element else None
        else:
            # It's likely a repository page
            contact_name = soup.find('a', class_='url fn').text.strip() if soup.find('a', class_='url fn') else None
        
        # Mobile number is typically not available on GitHub
        mobile_number = None
        
        # Use metadata as fallback
        if metadata:
            project_name = project_name or metadata.get('name')
            project_location = project_location or metadata.get('location')
            project_type = project_type or metadata.get('type')
            contact_name = contact_name or metadata.get('contact_name')
            mobile_number = mobile_number or metadata.get('mobile_number')
        
        return {
            "Project Name": project_name,
            "Project Location": project_location,
            "Project Type": project_type,
            "Contact Name": contact_name,
            "Mobile Number": mobile_number,
            "Source URL": url,
            "Extraction Date": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # Helper methods for extracting specific data fields
    def get_project_name(self, soup):
        """Extract project name from soup."""
        selectors = [
            'h1', 'h1.title', '.project-title', 'h2.title',
            'title', '.product-title', '.entry-title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.text.strip():
                return element.text.strip()
        
        return None
    
    def get_project_location(self, soup):
        """Extract project location from soup."""
        selectors = [
            '.location', 'span.location', '.project-location',
            'div[itemprop="location"]', '.address', '.location-info'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.text.strip():
                return element.text.strip()
        
        return None
    
    def get_project_type(self, soup):
        """Extract project type from soup."""
        selectors = [
            '.type', 'span.type', '.project-type',
            '.category', '.project-category', '.tags'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.text.strip():
                return element.text.strip()
        
        return None
    
    def get_contact_name(self, soup):
        """Extract contact name from soup."""
        selectors = [
            '.contact-name', 'span.contact-name', '.contact h3',
            '.contact-info .name', '.author-name', '.owner'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.text.strip():
                return element.text.strip()
        
        return None
    
    def get_mobile_number(self, soup):
        """Extract mobile number from soup."""
        # Try standard selectors
        selectors = [
            '.mobile-number', 'span.mobile-number', '.phone',
            '.contact-info .phone', '.tel', 'a[href^="tel:"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.text.strip():
                return element.text.strip()
        
        # Try to find phone number patterns in text
        import re
        phone_pattern = re.compile(r'(\+\d{1,3}[-.\s]?)?(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})')
        
        # Search in paragraphs and spans
        for element in soup.find_all(['p', 'span']):
            match = phone_pattern.search(element.text)
            if match:
                return match.group(0)
        
        return None


def load_websites_from_json(json_file):
    """
    Load website data from a JSON file.
    
    Args:
        json_file (str): Path to the JSON file.
        
    Returns:
        list: List of website data.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('websites', [])
    except Exception as e:
        logging.error(f"Error loading websites from {json_file}: {str(e)}")
        return []

def collect_data():
    """
    Collect data from websites defined in the configuration file.
    
    Returns:
        list: List of dictionaries containing extracted data.
    """
    json_path = 'src/config/websites.json'
    websites = load_websites_from_json(json_path)
    
    if not websites:
        logging.error(f"No websites found in {json_path}")
        return []
    
    scraper = WebScraper(websites)
    return scraper.fetch_data()

if __name__ == "__main__":
    # Configure basic logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Test the scraper
    websites = load_websites_from_json('src/config/websites.json')
    if websites:
        scraper = WebScraper(websites)
        data = scraper.fetch_data()
        print(f"Collected data from {len(data)} websites")
        for item in data:
            print(f"- {item.get('Project Name')}: {item.get('Source URL')}")
    else:
        print("No websites found in configuration")