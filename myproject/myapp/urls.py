# myapp/urls.py
from django.urls import path
from .views import survey_list, survey_detail, response_thank_you

urlpatterns = [
    path('surveys/', survey_list, name='survey_list'),
    path('survey/<int:survey_id>/', survey_detail, name='survey_detail'),
    path('response_thank_you/', response_thank_you, name='response_thank_you'),
]
