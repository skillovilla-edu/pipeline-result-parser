import json
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    # Extract HTML content from the event
    if 'pipeline_type' in event and event['pipeline_type'] == 'python':
        return html_parser_for_python_pipeline(event)
        
    if 'pipeline_type' in event and event['pipeline_type'] == 'node':
        return html_parser_for_node_pipeline(event)

    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Invalid pipeline_type'})
    }    

def html_parser_for_python_pipeline(event):
    if 'html_content' in event:
        html_content = event['html_content']
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'HTML content not found in event data'})
        }

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
        'statusCode': 200,
        'pipeline_type':'python',
        'body': json.dumps(table_data)
    }

def html_parser_for_node_pipeline(event):
    if 'html_content' in event:
        html_content = event['html_content']
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'HTML content not found in event data'})
        }

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
        'statusCode': 200,
        'pipeline_type':'node',
        'body': json.dumps(table_data)
    }


