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
        if len(columns) > 1:
            row_data = {
                'tests': int(columns[0].find('div', {'class': 'counter'}).text.strip()),
                'failures': int(columns[1].find('div', {'class': 'counter'}).text.strip()),
                'ignored': int(columns[2].find('div', {'class': 'counter'}).text.strip()),
                'duration': columns[3].find('div', {'class': 'counter'}).text.strip()
            }
            table_data.append(row_data)

    # Extract success rate
    success_rate_div = soup.find('div', {'id': 'successRate'})
    success_rate = success_rate_div.find('div', {'class': 'percent'}).text.strip()

    # Add success rate to each entry in table_data
    for row_data in table_data:
        row_data['success_rate'] = success_rate

    # Return the result as JSON
    return {
        'pipeline_type': pipeline_type,
        'data': table_data
    }

if __name__ == "__main__":
    import sys
    # Retrieve HTML content string from command line arguments
    html_content = sys.argv[1]
    # Retrieve pipeline_type variable from command line arguments
    pipeline_type = sys.argv[2]
    result = parse_html(html_content, pipeline_type)
    print(json.dumps(result, indent=4))
