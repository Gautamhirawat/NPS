# forms.py in myapp
from django import forms
from .models import Survey, Response

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'other_field1', 'other_field2']  # Add other fields
        
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['field1', 'field2']  # Add fields for responses
