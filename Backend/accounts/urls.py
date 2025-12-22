from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('me/', views.me),
    path('login/', views.login), 
    path('me/update/', views.update_profile),
    path('me/weight/', views.update_weight_settings),
    path('me/account/', views.update_account),
    path('me/delete/', views.delete_account),
    path("mypage/", views.mypage),
]
