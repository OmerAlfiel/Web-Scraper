from openpyxl import Workbook
from config.settings import EXCEL_CONFIG

def save_to_excel(data, file_path):
    """
    Saves the cleaned data to an Excel file.

    Parameters:
    data (DataFrame or list of dict): The cleaned data to be saved.
    file_path (str): The path where the Excel file will be saved.
    """
    # Create a new Excel workbook and select the active worksheet
    workbook = Workbook()
    worksheet = workbook.active

    # Define the header row
    headers = ["Project Name", "Project Location", "Project Type", "Contact Name", "Mobile Number", "Source URL"]
    worksheet.append(headers)

    # Check if data is a pandas DataFrame
    import pandas as pd
    if isinstance(data, pd.DataFrame):
        # If DataFrame, convert to records
        records = data.to_dict('records')
        for entry in records:
            worksheet.append([
                entry.get("Project Name", ""),
                entry.get("Project Location", ""),
                entry.get("Project Type", ""),
                entry.get("Contact Name", ""),
                entry.get("Mobile Number", ""),
                entry.get("Source URL", "")
            ])
    else:
        # If already a list of dictionaries
        for entry in data:
            worksheet.append([
                entry.get("Project Name", ""),
                entry.get("Project Location", ""),
                entry.get("Project Type", ""),
                entry.get("Contact Name", ""),
                entry.get("Mobile Number", ""),
                entry.get("Source URL", "")
            ])

    # Save the workbook to the specified file path
    workbook.save(file_path)
    print(f"Excel file saved to: {file_path}")

def export_to_excel(data):
    """
    Export cleaned data to Excel file using configuration settings.
    
    Parameters:
    data (list of dict or DataFrame): The cleaned data to be exported.
    
    Returns:
    str: The path to the saved Excel file.
    """
    output_file = EXCEL_CONFIG['output_file']
    save_to_excel(data, output_file)
    return output_file