# nps/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import os
import csv
from datetime import datetime

def home(request):
    return render(request, 'nps/home.html')

def save_survey(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Add timestamp to the data
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save data to a CSV file
        save_to_csv(data)

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

def save_to_csv(data):
    file_path = 'survey_data.csv'

    # Create or update the CSV file
    with open(file_path, 'a', newline='') as csv_file:
        fieldnames = ['timestamp', 'name', 'contact', 'likability', 'recommendation', 'feedback']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Check if the file is empty (write header if it is)
        if os.stat(file_path).st_size == 0:
            writer.writeheader()

        # Write the survey data to the file
        writer.writerow({
            'timestamp': data['timestamp'],
            'name': data['name'],
            'contact': data['contact'],
            'likability': data['likability'],
            'recommendation': data['recommendation'],
            'feedback': data['feedback']
        })
