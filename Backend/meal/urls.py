from django.urls import path
from .views import save_meal_data, recommend_dinner, select_meal, update_dinner_status, nutrition_calendar_month, nutrition_day_detail, predict_weight_change_view

urlpatterns = [
    path('save/', save_meal_data),
    path('recommend-dinner/', recommend_dinner),
    path('select-meal/', select_meal),
    path("dinner/status/", update_dinner_status),
    path("calendar/month/", nutrition_calendar_month),
    path("calendar/day/<int:date>/", nutrition_day_detail),
    path("predict-weight/", predict_weight_change_view),
]
