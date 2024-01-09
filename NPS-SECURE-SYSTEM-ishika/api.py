import requests
import json


from requests.api import _HeadersMapping
from requests.compat import urlsplit

#modules to connect api to database-postgresql
import psycopg2
from psycopg2 import sql


urls = ['https://api.devrev.ai/dev-users.self', 'https://app.devrev.ai/rev-users.create']

headers_list = [
    {
        'Authorization': 'Bearer your_token_here'
    },
    {
        'Authorization': 'Bearer your_other_token_here'
    }
]

def get_responses(urls, headers_list):
    responses = {}
    for url, headers in zip(urls, headers_list):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            responses[url] = response.json() # assuming the response is JSON
        else:
            responses[url] = None
    return responses

responses = get_responses(urls, headers_list)


conn = psycopg2.connect(
    dbname="your_database_name",
    user="your_username",
    password="your_password",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

for url, response in responses.items():
    if response.status_code == 200:
        data = response.json()

        user_id = data['rev_user']['id']
        email = data['rev_user']['email']
        full_name = data['rev_user']['full_name']
        phone_numbers = data['rev_user']['phone_numbers']

        insert = sql.SQL("INSERT INTO your_table (user_id, email, full_name, phone_numbers) VALUES (%s, %s, %s, %s)")
        cur.execute(insert, (user_id, email, full_name, phone_numbers))

conn.commit()

cur.close()
conn.close()