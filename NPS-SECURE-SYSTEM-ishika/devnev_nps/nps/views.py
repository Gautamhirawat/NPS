from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import admin
from django.urls import path, include
from .forms import SurveyForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nps.urls')),
]

def home(request):
    return render(request, 'nps/home.html')

def create_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save()
            # Additional logic if needed
            return redirect('survey_list')  # Redirect to survey list page
    else:
        form = SurveyForm()

    return render(request, 'create_survey.html', {'form': form})
