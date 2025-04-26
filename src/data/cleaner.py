# This file contains functions to clean and organize the extracted data.

import pandas as pd

def clean_data(raw_data):
    """
    Cleans and organizes the extracted data.

    Parameters:
    raw_data (list of dict): The raw data collected from the websites.

    Returns:
    pd.DataFrame: A DataFrame containing the cleaned data.
    """
    # Convert raw data to DataFrame
    df = pd.DataFrame(raw_data)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Fill missing values with appropriate defaults
    df.fillna({
        'Project Name': 'N/A',
        'Project Location': 'N/A',
        'Project Type': 'N/A',
        'Contact Name': 'N/A',
        'Mobile Number': 'N/A'
    }, inplace=True)

    # Organize columns in a specific order
    df = df[['Project Name', 'Project Location', 'Project Type', 'Contact Name', 'Mobile Number']]

    return df

def validate_data(df):
    """
    Validates the cleaned data to ensure it meets the required criteria.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the cleaned data.

    Returns:
    bool: True if data is valid, False otherwise.
    """
    # Check for any empty fields in critical columns
    if df[['Project Name', 'Contact Name', 'Mobile Number']].isnull().any().any():
        return False
    return True