import json
from bs4 import BeautifulSoup

def parse_html(html_content, pipeline_type):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the summary data
    summary_div = soup.find('div', {'id': 'summary'})
    summary_table = summary_div.find('table')
    summary_row = summary_table.find('tr')

    # Extract individual summary data
    columns = summary_row.find_all('td')
    row_data = {
        'tests': int(columns[0].find('div', {'id': 'tests'}).find('div', {'class': 'counter'}).text.strip()),
        'failures': int(columns[1].find('div', {'id': 'failures'}).find('div', {'class': 'counter'}).text.strip()),
        'ignored': int(columns[2].find('div', {'id': 'ignored'}).find('div', {'class': 'counter'}).text.strip()),
        'duration': columns[3].find('div', {'id': 'duration'}).find('div', {'class': 'counter'}).text.strip()
    }

    # Extract the success rate
    success_rate_div = soup.find('div', {'id': 'successRate'})
    success_rate = success_rate_div.find('div', {'class': 'percent'}).text.strip()
    row_data['success_rate'] = success_rate

    # Return the result as JSON
    return {
        'pipeline_type': pipeline_type,
        'data': row_data
    }

if __name__ == "__main__":
    import sys
    # Retrieve HTML content string from command line arguments
    html_content = sys.argv[1]
    # Retrieve pipeline_type variable from command line arguments
    pipeline_type = sys.argv[2]
    result = parse_html(html_content, pipeline_type)
    print(json.dumps(result, indent=4))
