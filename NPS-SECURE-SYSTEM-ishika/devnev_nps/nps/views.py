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

        # Save data to a CSV file
        save_to_csv(data)

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

def save_to_csv(data):
    file_path = 'survey_data.csv'

    # Create or update the CSV file
    with open(file_path, 'a', newline='') as csv_file:
        fieldnames = ['timestamp', 'name', 'contact', 'likability', 'recommendation', 'feedback', 'promoter', 'passive', 'detractor']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Check if the file is empty (write header if it is)
        if os.stat(file_path).st_size == 0:
            writer.writeheader()

        # Classify the respondent as Promoter, Passive, or Detractor
        likability = int(data['likability'])
        if likability >= 9:
            promoter = 1
            passive = 0
            detractor = 0
        elif likability >= 7:
            promoter = 0
            passive = 1
            detractor = 0
        else:
            promoter = 0
            passive = 0
            detractor = 1

     

        # Write the survey data to the file
        writer.writerow({
            'timestamp': data['timestamp'],
            'name': data['name'],
            'contact': data['contact'],
            'likability': likability,
            'recommendation': data['recommendation'],
            'feedback': data['feedback'],
            'promoter': promoter,
            'passive': passive,
            'detractor': detractor,
       
        })
