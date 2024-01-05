from django.shortcuts import render, get_object_or_404, redirect
from .models import Survey, Response
from .forms import SurveyForm, ResponseForm

def home(request):
    return render(request, 'home.html')


def survey_list(request):
    surveys = Survey.objects.all()
    return render(request, 'survey_list.html', {'surveys': surveys})

def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.survey = survey
            response.save()
            return redirect('response_thank_you')
    else:
        form = ResponseForm()
    return render(request, 'survey_detail.html', {'survey': survey, 'form': form})
