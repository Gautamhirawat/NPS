import requests
import json

#additional modules to connect api to database to map headers and urls
from requests.api import _HeadersMapping
from requests.compat import urlsplit

#modules to connect api to database-postgresql
import psycopg2
#from psycopg2 import sql

#to get data from form
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import YourModel  # replace with model name
from .forms import SignUpForm, LoginForm
# to be replaced with form name but we dont have a form as such; we have html????!!!!
#ideally, we have to have signup login survey forms to import

#authentication
from django.contrib.auth.hashers import check_password


#_____________________________________________________________________________
#HANDLING THE SIGNUP FORM
#GETTING THE DATA FROM THE FORM & SENDING THE DATA TO THE API THEN TO THE DATABASE
#____________________________________________________________________________

def form_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # replace register/signup form ie the respective class name in forms.py
        if form.is_valid():
            # Connect to your PostgreSQL database
            conn = psycopg2.connect(
                dbname="your_dbname",  # replace with your actual dbname
                user="your_username",  # replace with your actual username
                password="your_password",  # replace with your actual password
                host="your_host",  # replace with your actual host
                port="your_port"  # replace with your actual port 
            )
            cur = conn.cursor()

            # Make a POST request to the API to create a user
            url = 'https://app.devrev.ai/rev-users.create'
            headers = {
                'Authorization': 'Bearer your_token_here',
                'Content-Type': 'application/json'
            }
            data = {
                'rev_org': 'your_rev_org',  # replace with actual value
                'custom_fields': {},  # replace with actual value if needed
                'custom_schema_fragments': ['your_schema_fragment1', 'your_schema_fragment2'],  # replace with actual values
                'description': 'your_description',  # replace with actual value
                'display_name': 'your_display_name',  # replace with actual value
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
                'external_ref': 'your_external_ref',  # replace with actual value
                'phone_numbers': ['your_phone_number1', 'your_phone_number2']  # replace with actual values
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                # Insert API response into the database
                insert_query = "INSERT INTO your_table (username, email, password) VALUES (%s, %s, %s)"  # replace with your actual table and column names
                cur.execute(insert_query, (json.dumps(response.json()),))  # assuming the response is JSON
                conn.commit()

            cur.close()
            conn.close()

            return HttpResponseRedirect('/login.html')  # replace with your actual thanks URL or sign in / login URL

    else:
        form = SignUpForm()  # replace with your actual form initial- this one is signup form

    return render(request, 'signup.html', {'form': form})  # replace with your actual template name- register/signup

#_____________________________________________________________________________
#HANDLING THE LOGIN FORM
#GETTING THE DATA FROM THE FORM & SENDING THE DATA TO THE API TO MATCH THE DATA IN THE DATABASE
#____________________________________________________________________________

def form_view(request):
    if request.method == 'GET':
        form = LoginForm(request.GET)  # replace with form - login form
        if form.is_valid():
            # Make a GET request to the API to get a user
            url = f'https://app.devrev.ai/rev-users.get?id={form.cleaned_data["username"]}'  # replace 'username' with the actual user ID field
            headers = {
                'Accept': 'application/json',
                'Authorization': 'Bearer your_token_here'  # replace with your actual token
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                # User exists in the database
                user_data = response.json()
                if check_password(form.cleaned_data['password'], user_data['password']):
                # Password is correct
                    return HttpResponseRedirect('/survey.html')  # replace with your response URL, wherevr you want to redirect after successful login
                else:
                    # Password is incorrect
                    form.add_error('password', 'Incorrect password')
            elif response.status_code == 404:
                # User does not exist in the database
                # Add an error to the form and display the login page again
                form.add_error(None, 'User does not exist')
                

    else:
        form = LoginForm()  # replace with your actual form- this one is login form

    return render(request, 'login.html', {'form': form})  # replace with your actual template name









#kindly ignore this part of the code; anything and everything below this is just for reference and is not used in the project
'''
THEN DID THIS AS WE WILL HAVE TO HANDLE ALL FORMS DIFFERENTLY

def form_view(request):
    if request.method == 'POST':
        form = YourForm(request.POST)  # replace with your actual form
        if form.is_valid():
            # Create an instance of your model with the form data
            instance = YourModel(**form.cleaned_data)
            instance.save()  # Save the instance to the database

            # Make requests to the API
            urls = ['https://api.devrev.ai/dev-users.self', 'https://app.devrev.ai/rev-users.create']
            headers_list = [
                {
                    'Authorization': 'Bearer your_token_here'
                },
                {
                    'Authorization': 'Bearer your_other_token_here'
                }
            ]
            for url, headers in zip(urls, headers_list):
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    # Do something with the response, e.g. update the instance
                    instance.api_response = response.json()  # assuming the response is JSON and your model has an api_response field
                    instance.save()

            return HttpResponseRedirect('/success_url/')  # replace with thanks page

    else:
        form = YourForm()  #to be replaced with form but we dont have a form as such we have html????!!!!

    return render(request, 'thank_you.html', {'form': form})  # responds with thank you page

'''

'''
ORIGINALLY DID THIS BUT THE FORM WAS NOT INVOLVED

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

'''





