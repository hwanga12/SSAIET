# accounts/views.py
# accounts/views.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login as django_login
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
# 회원가입
# -------------------------
@api_view(['POST'])
def signup(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "회원가입이 완료되었어요!"}, status=201)
    return Response(serializer.errors, status=400)

# -------------------------
# 내 정보 조회
# -------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def me(request):
    return Response(UserSerializer(request.user).data)

# -------------------------
# 전체 프로필 수정
# -------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = ProfileUpdateSerializer(instance=user, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

# -------------------------
# 신체 정보 일부 수정 (PATCH)
# -------------------------
@api_view(['PATCH'])
@permission_classes([IsAuthenticated]) # 보안을 위해 추가 권장
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
# 계정 정보 수정 (아이디/비밀번호)
# -------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_account(request):
    user = request.user
    serializer = AccountUpdateSerializer(
        instance=user,
        data=request.data,
        partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "계정 정보가 변경되었습니다."}, status=200)
    return Response(serializer.errors, status=400)

# -------------------------
# 계정 삭제
# -------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    user.delete()
    return Response(
        {"message": "그동안 이용해 주셔서 감사합니다. 계정이 삭제되었습니다."},
        status=status.HTTP_200_OK
    )

# -------------------------
# 로그인 (이메일 제거 완료)
# -------------------------
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"detail": "아이디 또는 비밀번호를 다시 확인해 주세요."}, status=status.HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(user)

    # 응답 데이터에서 email 삭제
    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "username": user.username,
        "name": user.name,
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
    return Response({"message": "로그아웃 되었습니다."}, status=200)

# ... (마이페이지 로직은 동일하므로 생략)

from community.models import CommunityPost, PostComment, PostLike
from community.serializers import CommunityPostSerializer, PostCommentSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mypage(request):
    user = request.user

    # ✅ 내가 쓴 게시글
    my_posts = CommunityPost.objects.filter(author=user)

    # ✅ 내가 쓴 댓글
    my_comments = PostComment.objects.filter(author=user)

    # ✅ 내가 좋아요한 게시글
    liked_post_ids = PostLike.objects.filter(user=user).values_list("post_id", flat=True)
    liked_posts = CommunityPost.objects.filter(id__in=liked_post_ids)

    return Response({
        "counts": {
            "post_count": my_posts.count(),
            "comment_count": my_comments.count(),
            "like_count": liked_post_ids.count(),
        },
        "posts": CommunityPostSerializer(
            my_posts,
            many=True,
            context={"request": request}
        ).data,
        "comments": PostCommentSerializer(
            my_comments,
            many=True,
            context={"request": request}
        ).data,
        "liked_posts": CommunityPostSerializer(
            liked_posts,
            many=True,
            context={"request": request}
        ).data,
    })
