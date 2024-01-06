from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import SignUpView, LoginView, LogoutView, HomeView

urlpatterns = [
    path('', views.home, name='home'),
    path('thank_you/', TemplateView.as_view(template_name='thank_you.html'), name='thank_you'),
    path('save_survey/', views.save_survey, name='save_survey'),  # Add this line
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
