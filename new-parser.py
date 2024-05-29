import json
from bs4 import BeautifulSoup

def parse_html(html_content, pipeline_type):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the summary data
    summary_div = soup.find('div', {'id': 'summary'})
    summary_table = summary_div.find('table')
    summary_rows = summary_table.find_all('tr')

    # Extract individual summary data
    summary_data = {}
    for row in summary_rows:
        columns = row.find_all('td')
        if columns:
            tests_div = columns[0].find('div', {'id': 'tests'})
            failures_div = columns[1].find('div', {'id': 'failures'})
            ignored_div = columns[2].find('div', {'id': 'ignored'})
            duration_div = columns[3].find('div', {'id': 'duration'})

            if tests_div and failures_div and ignored_div and duration_div:
                summary_data = {
                    'tests': int(tests_div.find('div', {'class': 'counter'}).text.strip()),
                    'failures': int(failures_div.find('div', {'class': 'counter'}).text.strip()),
                    'ignored': int(ignored_div.find('div', {'class': 'counter'}).text.strip()),
                    'duration': duration_div.find('div', {'class': 'counter'}).text.strip()
                }

    # Extract the success rate
    success_rate_div = soup.find('div', {'id': 'successRate'})
    success_rate = success_rate_div.find('div', {'class': 'percent'}).text.strip()
    summary_data['success_rate'] = success_rate

    # Return the result as JSON
    return {
        'pipeline_type': pipeline_type,
        'data': summary_data
    }

if __name__ == "__main__":
    import sys
    # Retrieve HTML content string from command line arguments
    html_content = sys.argv[1]
    # Retrieve pipeline_type variable from command line arguments
    pipeline_type = sys.argv[2]
    result = parse_html(html_content, pipeline_type)
    print(json.dumps(result, indent=4))
