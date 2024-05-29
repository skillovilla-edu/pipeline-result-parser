import json
from bs4 import BeautifulSoup

def parse_html(html_content, pipeline_type):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the specific table
    specific_table = soup.find('div', {'id': 'summary'}).find('table')

    # Extract table data
    table_data = []
    for row in specific_table.find_all('tr'):
        columns = row.find_all('td')
        row_data = {
            'tests': int(columns[0].find('div', {'class': 'counter'}).text.strip()),
            'failures': int(columns[1].find('div', {'class': 'counter'}).text.strip()),
            'ignored': int(columns[2].find('div', {'class': 'counter'}).text.strip()),
            'duration': columns[3].find('div', {'class': 'counter'}).text.strip()
        }
        table_data.append(row_data)

    # Return the result as JSON
    return {
        'pipeline_type': pipeline_type,
        'data': table_data
    }

result = parse_html(html_string, pipeline_type)
print(json.dumps(result, indent=4))