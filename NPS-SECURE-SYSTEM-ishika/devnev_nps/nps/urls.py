from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('thank_you/', TemplateView.as_view(template_name='thank_you.html'), name='thank_you'),
    path('save_survey/', views.save_survey, name='save_survey'),  # Add this line

]
