"""
Data Cleaner Module

This file contains functions to clean and organize the extracted data.
"""

import pandas as pd
import re
import logging


def clean_data(raw_data):
    """
    Cleans and organizes the extracted data.

    Parameters:
    raw_data (list of dict): The raw data collected from the websites.

    Returns:
    pd.DataFrame: A DataFrame containing the cleaned data.
    """
    if not raw_data:
        logging.warning("No data to clean")
        return pd.DataFrame()
    
    try:
        # Convert raw data to DataFrame
        df = pd.DataFrame(raw_data)
        
        # Basic cleaning
        df = basic_cleaning(df)
        
        # Format phone numbers
        if 'Mobile Number' in df.columns:
            df['Mobile Number'] = df['Mobile Number'].apply(format_phone_number)
        
        # Add data quality indicators
        df = add_data_quality_indicators(df)
        
        # Organize columns in a specific order
        columns = [
            'Project Name', 'Project Location', 'Project Type', 
            'Contact Name', 'Mobile Number', 'Source URL', 
            'Extraction Date', 'Data Quality Score'
        ]
        
        # Only include columns that exist in df
        existing_columns = [col for col in columns if col in df.columns]
        df = df[existing_columns]
        
        return df
    
    except Exception as e:
        logging.error(f"Error cleaning data: {str(e)}")
        # Return empty DataFrame if cleaning fails
        return pd.DataFrame()


def basic_cleaning(df):
    """Basic data cleaning operations."""
    # Remove duplicates
    df = df.drop_duplicates(subset=['Source URL'], keep='first')
    
    # Remove rows with missing project names (essential field)
    df = df.dropna(subset=['Project Name'])
    
    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        if col in df:
            df[col] = df[col].astype(str).str.strip()
    
    # Standardize project type names
    if 'Project Type' in df.columns:
        df['Project Type'] = df['Project Type'].apply(standardize_project_type)
    
    # Fill missing values with appropriate defaults
    default_values = {
        'Project Location': 'Unknown',
        'Project Type': 'Miscellaneous',
        'Contact Name': 'Unknown',
        'Mobile Number': 'Not provided'
    }
    
    for col, default in default_values.items():
        if col in df.columns:
            df[col] = df[col].fillna(default)
            # Replace empty strings with default
            df.loc[df[col] == '', col] = default
    
    return df


def format_phone_number(number):
    """Format phone numbers consistently."""
    if pd.isna(number) or not number:
        return "Not provided"
    
    # Remove non-digit characters
    digits = re.sub(r'\D', '', str(number))
    
    # Check if we have a valid number of digits
    if len(digits) == 10:  # US format
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':  # US with country code
        return f"{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    elif len(digits) == 12 and digits[:3] == '966':  # KSA format
        return f"+{digits[:3]}-{digits[3:5]}-{digits[5:]}"
    elif 8 <= len(digits) <= 15:  # Other international format
        if len(digits) > 10:
            country_code = digits[:len(digits)-10]
            return f"+{country_code}-{digits[len(digits)-10:len(digits)-7]}-{digits[len(digits)-7:len(digits)-4]}-{digits[len(digits)-4:]}"
        else:
            # For shorter numbers, just group them
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    
    # If nothing else matches, return as is
    return number


def standardize_project_type(project_type):
    """Standardize project type names."""
    if pd.isna(project_type) or not project_type:
        return "Miscellaneous"
    
    project_type = project_type.lower()
    
    # Map common variations to standard types
    type_mapping = {
        'web': 'Web Development',
        'website': 'Web Development',
        'app': 'Mobile App',
        'application': 'Software Development',
        'software': 'Software Development',
        'mobile': 'Mobile App',
        'android': 'Mobile App',
        'ios': 'Mobile App',
        'design': 'Design',
        'graphic': 'Graphic Design',
        'ui': 'UI/UX Design',
        'ux': 'UI/UX Design',
        'car': 'Automotive',
        'auto': 'Automotive',
        'vehicle': 'Automotive',
        'portfolio': 'Portfolio',
    }
    
    for key, value in type_mapping.items():
        if key in project_type:
            return value
    
    # If no match, capitalize the original type
    return project_type.title()


def add_data_quality_indicators(df):
    """Add data quality indicators to the DataFrame."""
    # Calculate a simple data quality score (0-100)
    quality_scores = []
    
    for _, row in df.iterrows():
        score = 0
        
        # Project Name (essential) - 30 points
        if not pd.isna(row.get('Project Name')) and row.get('Project Name', '') != '':
            score += 30
        
        # Contact information - 40 points (20 each)
        if not pd.isna(row.get('Contact Name')) and row.get('Contact Name', '') not in ['', 'Unknown']:
            score += 20
            
        if not pd.isna(row.get('Mobile Number')) and row.get('Mobile Number', '') not in ['', 'Not provided']:
            score += 20
        
        # Other fields - 30 points (15 each)
        if not pd.isna(row.get('Project Location')) and row.get('Project Location', '') not in ['', 'Unknown']:
            score += 15
            
        if not pd.isna(row.get('Project Type')) and row.get('Project Type', '') not in ['', 'Miscellaneous']:
            score += 15
        
        quality_scores.append(score)
    
    df['Data Quality Score'] = quality_scores
    
    return df


def validate_data(df):
    """
    Validates the cleaned data to ensure it meets the required criteria.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the cleaned data.

    Returns:
    bool: True if data is valid, False otherwise.
    """
    # Check if DataFrame is empty
    if df.empty:
        logging.warning("Data validation failed: DataFrame is empty")
        return False
    
    # Check for minimum required columns
    required_columns = ['Project Name', 'Source URL']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        logging.warning(f"Data validation failed: Missing required columns {missing_columns}")
        return False
    
    # Check for minimum data quality
    if 'Data Quality Score' in df.columns:
        avg_quality = df['Data Quality Score'].mean()
        if avg_quality < 40:  # Arbitrary threshold
            logging.warning(f"Data validation warning: Low average data quality score ({avg_quality})")
    
    # Check for minimum number of records
    if len(df) < 1:
        logging.warning("Data validation failed: No records found after cleaning")
        return False
    
    return True


if __name__ == "__main__":
    # Test the cleaner with some sample data
    sample_data = [
        {
            "Project Name": "Test Project 1",
            "Project Location": "Location A",
            "Project Type": "web development",
            "Contact Name": "John Doe",
            "Mobile Number": "123-456-7890",
            "Source URL": "https://example.com/1"
        },
        {
            "Project Name": "Test Project 2",
            "Project Location": "",
            "Project Type": "mobile app",
            "Contact Name": "",
            "Mobile Number": "9876543210",
            "Source URL": "https://example.com/2"
        }
    ]
    
    cleaned_data = clean_data(sample_data)
    print(cleaned_data)