# urls.py

from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('profile/', views.profile, name='profile'),
    path('weight-settings/', views.weight_settings, name='weight_settings'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('account/edit/', views.account_edit, name='account_edit'),
    path('delete/confirm/', views.delete_confirm, name='delete_confirm'),
    path('delete/', views.account_delete, name='account_delete'),
]