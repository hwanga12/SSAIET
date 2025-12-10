# accounts/views.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .serializers import (
    UserCreateSerializer,
    UserSerializer,
    ProfileUpdateSerializer,
    AccountUpdateSerializer
)

from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# -------------------------
# 회원가입 (제한 없음)
# -------------------------
@api_view(['POST'])
def signup(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Django 로그인 제거!
        # login(request, user)

        return Response({"message": "signup success"}, status=201)

    return Response(serializer.errors, status=400)

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
@permission_classes([IsAuthenticated]) # 이 데코레이터가 반드시 있어야 합니다.
def update_profile(request):
    user = request.user
    # 👇 instance= 키워드를 명시적으로 사용하세요.
    serializer = ProfileUpdateSerializer(instance=user, data=request.data)

    if serializer.is_valid(raise_exception=True): # raise_exception=True를 사용하면 400 응답이 간결해집니다.
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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
@permission_classes([IsAuthenticated])
def update_account(request):
    user = request.user
    serializer = AccountUpdateSerializer(
        instance=user,
        data=request.data,
        partial=True  # 선택 입력 가능
    )

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "account updated"}, status=200)

    return Response(serializer.errors, status=400)

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

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),

        # 🔥 여기에 사용자 정보 추가
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "height": user.height,
        "current_weight": user.current_weight,
        "target_weight": user.target_weight,
        "muscle_mass": user.muscle_mass,
        "body_fat": user.body_fat,
        "age": user.age,
        "gender": user.gender,
        "allergies": user.allergies,
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    JWT 기반에서는 서버가 할 일이 거의 없지만,
    클라이언트가 refresh token을 보내면 DB에서 무효화할 수도 있음.
    여기서는 단순히 성공 응답만 반환.
    """
    return Response({"message": "logout success"}, status=200)
