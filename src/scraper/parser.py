# parser.py

def parse_project_data(raw_data):
    """
    Parses the raw HTML data to extract project information.

    Args:
        raw_data (str): The raw HTML content of the webpage.

    Returns:
        dict: A dictionary containing the extracted project information.
    """
    project_info = {
        "Project Name": None,
        "Project Location": None,
        "Project Type": None,
        "Contact Name": None,
        "Mobile Number": None
    }

    # Implement parsing logic here
    # Example: Use BeautifulSoup to parse the HTML and extract the required fields

    return project_info

def parse_multiple_projects(raw_data_list):
    """
    Parses a list of raw HTML data to extract project information for multiple projects.

    Args:
        raw_data_list (list): A list of raw HTML content from multiple webpages.

    Returns:
        list: A list of dictionaries containing the extracted project information.
    """
    projects = []
    for raw_data in raw_data_list:
        project_info = parse_project_data(raw_data)
        projects.append(project_info)

    return projects