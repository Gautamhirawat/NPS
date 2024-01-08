import requests
import json

#modules to connect api to database-postgresql
import psycopg2
from psycopg2 import sql




url = ['https://api.devrev.ai/dev-users.self', 'https://app.devrev.ai/rev-users.create']

headers_list = [
    {
        'Authorization': 'Bearer your_token_here'
    },
    {
        'Authorization': 'Bearer your_other_token_here'
    }
]



response = requests.get(url, headers=headers)



if response.status_code == 200:
    # You can access the response content with response.text
    print(response.text)
else:
    print(f'Request failed with status code {response.status_code}')



payload = json.dumps({
  "rev_org": "<string>",
  "custom_fields": {},
  "custom_schema_fragments": [
    "<string>",
    "<string>"
  ],
  "description": "<string>",
  "display_name": "<string>",
  "email": "<string>",
  "external_ref": "<string>",
  "phone_numbers": [
    "<string>",
    "<string>"
  ]
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': '<API Key>'
}

def get_responses(urls, headers_list):
    responses = {}
    for url, headers in zip(urls, headers_list):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            responses[url] = response.json()  # assuming the response is JSON
        else:
            responses[url] = None
    return responses

responses = get_responses(urls, headers_list)




# Establish a connection to the database
conn = psycopg2.connect(
    dbname="your_database_name",
    user="your_username",
    password="your_password",
    host="localhost",
    port="5432"
)

# Create a cursor object
cur = conn.cursor()

# Process each response and store the data in the database
for url, response in responses.items():
    if response.status_code == 200:
        data = response.json()

# Assuming the responses is a dictionary where the values are JSON objects
for url, data in responses.items():
    if data is not None:
        # Extract the data from the JSON
        user_id = data['rev_user']['id']
        email = data['rev_user']['email']
        full_name = data['rev_user']['full_name']
        phone_numbers = data['rev_user']['phone_numbers']
        # Insert the data into the database
        insert = sql.SQL("INSERT INTO your_table (user_id, email, full_name, phone_numbers) VALUES (%s, %s, %s, %s)")
        cur.execute(insert, (user_id, email, full_name, phone_numbers))

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()