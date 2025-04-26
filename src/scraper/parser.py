"""
Web Scraper Parser Module

This module handles the parsing of raw HTML data to extract structured information.
It provides utilities for parsing different types of website structures.
"""

from bs4 import BeautifulSoup
import re
import logging
from urllib.parse import urlparse


def parse_project_data(raw_data, url):
    """
    Parses the raw HTML data to extract project information.

    Args:
        raw_data (str): The raw HTML content of the webpage.
        url (str): URL of the webpage being parsed.

    Returns:
        dict: A dictionary containing the extracted project information.
    """
    project_info = {
        "Project Name": None,
        "Project Location": None,
        "Project Type": None,
        "Contact Name": None,
        "Mobile Number": None,
        "Source URL": url
    }
    
    try:
        soup = BeautifulSoup(raw_data, 'html.parser')
        domain = urlparse(url).netloc
        
        # Choose parser based on domain
        if 'sudancar.com' in domain:
            project_info = parse_sudancar(soup, project_info)
        elif 'github.com' in domain:
            project_info = parse_github(soup, project_info)
        elif 'vercel.app' in domain:
            project_info = parse_portfolio(soup, project_info)
        else:
            # Generic parser
            project_info = parse_generic(soup, project_info)
            
        return project_info
    
    except Exception as e:
        logging.error(f"Error parsing data from {url}: {str(e)}")
        return project_info


def parse_sudancar(soup, project_info):
    """Parse data from Sudancar website."""
    try:
        # Extract project name
        title_elem = soup.find('h1', class_='title') or soup.find('h1')
        if title_elem:
            project_info["Project Name"] = title_elem.text.strip()
        
        # Extract location
        location_elem = soup.find('div', class_='location') or soup.find('span', class_='location')
        if location_elem:
            project_info["Project Location"] = location_elem.text.strip()
        
        # Extract project type (car type/model)
        type_elem = soup.find('div', class_='car-model') or soup.find('span', class_='car-type')
        if type_elem:
            project_info["Project Type"] = type_elem.text.strip()
        
        # Extract contact info
        contact_elem = soup.find('div', class_='contact-info')
        if contact_elem:
            name_elem = contact_elem.find('h3') or contact_elem.find('strong')
            if name_elem:
                project_info["Contact Name"] = name_elem.text.strip()
            
            phone_elem = contact_elem.find('a', href=lambda x: x and x.startswith('tel:'))
            if phone_elem:
                project_info["Mobile Number"] = phone_elem.text.strip()
    
    except Exception as e:
        logging.error(f"Error parsing Sudancar data: {str(e)}")
    
    return project_info


def parse_github(soup, project_info):
    """Parse data from GitHub website."""
    try:
        # Extract project name (repository name or profile name)
        name_elem = soup.find('h1', class_='d-inline') or soup.find('h1')
        if name_elem:
            project_info["Project Name"] = name_elem.text.strip()
        
        # Set project type
        project_info["Project Type"] = "Software Development"
        
        # For profile pages
        vcard = soup.find('div', class_='vcard-details')
        if vcard:
            location_elem = vcard.find('li', itemprop='homeLocation')
            if location_elem:
                project_info["Project Location"] = location_elem.text.strip()
        
        # For repository pages
        repo_author = soup.find('a', attrs={'rel': 'author'})
        if repo_author:
            project_info["Contact Name"] = repo_author.text.strip()
    
    except Exception as e:
        logging.error(f"Error parsing GitHub data: {str(e)}")
    
    return project_info


def parse_portfolio(soup, project_info):
    """Parse data from portfolio website."""
    try:
        # Extract project name
        title_elem = soup.find('h1') or soup.find('title')
        if title_elem:
            project_info["Project Name"] = title_elem.text.strip()
        
        # Extract contact info
        contact_section = soup.find('section', id='contact') or soup.find('div', class_='contact')
        if contact_section:
            name_elem = contact_section.find('h2') or contact_section.find('h3')
            if name_elem:
                project_info["Contact Name"] = name_elem.text.strip()
            
            # Look for phone number in contact section
            phone_pattern = re.compile(r'(\+\d{1,3}[-.\s]?)?(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})')
            for paragraph in contact_section.find_all(['p', 'span', 'a']):
                match = phone_pattern.search(paragraph.text)
                if match:
                    project_info["Mobile Number"] = match.group(0)
                    break
        
        # Extract location if available
        location_elem = soup.find('div', class_='location') or soup.find('span', class_='location')
        if location_elem:
            project_info["Project Location"] = location_elem.text.strip()
        
        # Extract project type
        project_info["Project Type"] = "Portfolio Website"
    
    except Exception as e:
        logging.error(f"Error parsing portfolio data: {str(e)}")
    
    return project_info


def parse_generic(soup, project_info):
    """Generic parser for unknown website structures."""
    try:
        # Try to extract project name from title or h1
        title_elem = soup.find('h1') or soup.find('title')
        if title_elem:
            project_info["Project Name"] = title_elem.text.strip()
        
        # Look for location information
        location_keywords = ['location', 'address', 'place']
        for keyword in location_keywords:
            elements = soup.find_all(['div', 'span', 'p'], class_=lambda x: x and keyword in x.lower())
            if elements:
                project_info["Project Location"] = elements[0].text.strip()
                break
        
        # Look for contact information
        contact_keywords = ['contact', 'get in touch', 'reach us']
        contact_section = None
        
        # Find contact section
        for keyword in contact_keywords:
            sections = soup.find_all(['section', 'div'], id=lambda x: x and keyword in x.lower())
            sections.extend(soup.find_all(['section', 'div'], class_=lambda x: x and keyword in x.lower()))
            if sections:
                contact_section = sections[0]
                break
        
        if contact_section:
            # Look for name
            name_elem = contact_section.find(['h2', 'h3', 'h4', 'strong'])
            if name_elem:
                project_info["Contact Name"] = name_elem.text.strip()
            
            # Look for phone number
            phone_pattern = re.compile(r'(\+\d{1,3}[-.\s]?)?(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})')
            for elem in contact_section.find_all(['p', 'span', 'a']):
                match = phone_pattern.search(elem.text)
                if match:
                    project_info["Mobile Number"] = match.group(0)
                    break
        
        # Try to determine project type from meta tags or content
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords and meta_keywords.get('content'):
            keywords = meta_keywords['content'].split(',')
            project_info["Project Type"] = keywords[0].strip()
        else:
            # Default generic type
            project_info["Project Type"] = "Website"
    
    except Exception as e:
        logging.error(f"Error in generic parser: {str(e)}")
    
    return project_info


def parse_multiple_projects(raw_data_list, urls):
    """
    Parses a list of raw HTML data to extract project information for multiple projects.

    Args:
        raw_data_list (list): A list of raw HTML content from multiple webpages.
        urls (list): A list of URLs corresponding to the raw data.

    Returns:
        list: A list of dictionaries containing the extracted project information.
    """
    if len(raw_data_list) != len(urls):
        logging.error("Mismatch between raw data list and URLs list lengths")
        return []
    
    projects = []
    for i, raw_data in enumerate(raw_data_list):
        url = urls[i] if i < len(urls) else "unknown"
        project_info = parse_project_data(raw_data, url)
        projects.append(project_info)
    
    return projects