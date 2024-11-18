from django.urls import path
from .views import home, profile, RegisterView, layoff_prediction_form, success_view

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('form/', layoff_prediction_form, name='layoff_prediction_form'),
    path('success/', success_view, name='success'),
]
