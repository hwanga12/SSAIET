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

    ## 🌟 JWT 인증 경로 추가 🌟
    # 1. 토큰 발급 (로그인): username과 password를 보내면 Access/Refresh 토큰을 받습니다.
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # 2. 토큰 갱신: 만료된 Access 토큰을 Refresh 토큰으로 갱신하여 새 Access 토큰을 받습니다.
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('meal/', include('meal.urls')),
]