from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API 엔드포인트
    path('api/accounts/', include('accounts.urls')),

    # JWT 인증
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 식단
    path('meal/', include('meal.urls')),

    # ✅ 커뮤니티
    path('api/community/', include('community.urls')),
    
]
