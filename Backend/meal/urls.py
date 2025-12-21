from django.urls import path
from .views import save_meal_data, recommend_dinner, select_meal, update_dinner_status, dinner_calendar

urlpatterns = [
    path('save/', save_meal_data),
    path('recommend-dinner/', recommend_dinner),
    path('select-meal/', select_meal),
    path("dinner/status/", update_dinner_status),
    path('calendar/', dinner_calendar),  # 추가된 부분

]
