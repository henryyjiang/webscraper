import requests
import json
import pandas as pd

# Headers (if required)
headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache'
}

api_key = ''
csv_file = 'contact_data.csv'
url = 'https://api.apollo.io/v1/people/match'
reveal_personal_emails = True

# variables for names in the CSV
first_name = "first_name"
last_name = "last_name"
email = "email"
organization_name = "organization"
domain = "domain"

try:
    df = pd.read_csv(csv_file, sep=';')

    for index, row in df.iterrows():
        # Request payload (data to be sent)
        payload = {
            "api_key": api_key,
            "reveal_personal_emails": reveal_personal_emails
        }
        # Check if each key exists in the row and add the key-value pair to the payload
        if pd.notnull(row[first_name]):
            payload['first_name'] = row[first_name]

        if last_name in row and pd.notnull(row[last_name]):
            payload['last_name'] = row[last_name]

        if email in row and pd.notnull(row[email]):
            payload['email'] = row[email]

        if organization_name in row and pd.notnull(row[organization_name]):
            payload['organization_name'] = row[organization_name]

        if domain in row and pd.notnull(row[domain]):
            payload['domain'] = row[domain]

        print(payload)

        # Send POST request
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            # Remove specific parts from the response
            filtered_data = []
            match_data_list = data['person']
            filtered_item = {
                key: value['sanitized_phone'] if isinstance(value, dict) and len(value) > 0 and 'sanitized_phone' in value
                else (value['name']) if isinstance(value, dict) and 'name' in value else value
                for key, value in match_data_list.items()
                if  key in ['first_name', 'last_name', 'title',
                           'headline', 'email', 'state', 'city',
                           'country', 'organization', 'contact',
                           'departments', 'subdepartments', 'seniority']
            }
            print(filtered_item)

            if first_name == None:
                df = pd.concat([df, row], ignore_index=True)
            else:
                df = pd.concat([df, filtered_data], ignore_index=True)

        else:
            # Print the error message
            print(f'Request failed with status code {response.status_code}: {response.text}')

    # Save the combined DataFrame back to the CSV file
    #df.to_csv(csv_file, index=False, sep=';')
    #print(f'Response data saved as {csv_file}')

    df.to_csv('test.csv', index=False, sep=';')
    print('Response data saved as test.csv')

except requests.exceptions.RequestException as e:
    # Print the error message if an exception occurs
    print(f'Request failed: {e}')
