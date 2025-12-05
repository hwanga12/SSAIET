from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API 엔드포인트들
    path('api/accounts/', include('accounts.urls')),
    path('api/fitplan/', include('fitplan.urls')),
]