from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('me/', views.me),
    path('me/update/', views.update_profile),
    path('me/weight/', views.update_weight_settings),
    path('me/password/', views.change_password),
    path('me/delete/', views.delete_account),
]