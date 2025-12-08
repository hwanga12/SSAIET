from django.urls import path
from .views import save_meal_data

urlpatterns = [
    path('save/', save_meal_data),
]
