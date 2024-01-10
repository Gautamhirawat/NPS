# nps/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import os
import csv
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import SignUpForm, LoginForm

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')




class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Handle user registration logic and create a new user
            # ...

            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')

        return render(request, 'signup.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')

        return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

def home(request):
    return render(request, 'nps/home.html')

def save_survey(request):
    try:
        if request.method == 'POST':
            # Decode the request body before loading it as JSON
            request_body = request.body.decode('utf-8')
            data = json.loads(request_body)

            # Save data to a CSV file
            save_to_csv(data)

            return JsonResponse({'status': 'success'})
    except json.JSONDecodeError as e:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

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
        promoter, passive, detractor = 0, 0, 0

        if likability >= 9:
            promoter = 1
        elif likability >= 7:
            passive = 1
        else:
            detractor = 1

        # Write the survey data to the file
        writer.writerow({
            'timestamp': data.get('timestamp', ''),
            'name': data.get('name', ''),
            'contact': data.get('contact', ''),
            'likability': likability,
            'recommendation': data.get('recommendation', ''),
            'feedback': data.get('feedback', ''),
            'promoter': promoter,
            'passive': passive,
            'detractor': detractor,
        })
