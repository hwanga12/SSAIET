# accounts/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    UserCreateSerializer,
    UserSerializer,
    ProfileUpdateSerializer
)

from django.contrib.auth import get_user_model

User = get_user_model()

# -------------------------
# 회원가입 (제한 없음)
# -------------------------
@api_view(['POST'])
def signup(request):
    serializer = UserCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------
# 내 정보 조회 (제한 없음)
# -------------------------
@api_view(['GET'])
def me(request):
    return Response(UserSerializer(request.user).data)


# -------------------------
# 전체 프로필 수정 (제한 없음)
# -------------------------
@api_view(['PUT'])
def update_profile(request):
    user = request.user
    serializer = ProfileUpdateSerializer(user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------
# weight settings 일부 수정 (PATCH)
# -------------------------
@api_view(['PATCH'])
def update_weight_settings(request):
    user = request.user
    serializer = ProfileUpdateSerializer(
        user,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------
# 비밀번호 변경 (제한 없음)
# -------------------------
@api_view(['PUT'])
def change_password(request):
    user = request.user
    new_pw = request.data.get("password")

    if not new_pw:
        return Response(
            {"error": "password required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(new_pw)
    user.save()

    return Response(
        {"message": "password updated"},
        status=status.HTTP_200_OK
    )
# -------------------------
# 계정 삭제 (DELETE)
# -------------------------
@api_view(['DELETE'])
def delete_account(request):
    user = request.user
    
    # 익명 사용자라도 테스트 위해 그냥 진행
    if user.is_anonymous:
        return Response(
            {"error": "anonymous user cannot be deleted"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.delete()
    return Response(
        {"message": "Account deleted successfully"},
        status=status.HTTP_200_OK
    )
