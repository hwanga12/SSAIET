from django.urls import path
from .views import save_meal_data, recommend_dinner, select_meal

urlpatterns = [
    path('save/', save_meal_data),
    path('recommend-dinner/', recommend_dinner),
    path('select-meal/', select_meal),
]
