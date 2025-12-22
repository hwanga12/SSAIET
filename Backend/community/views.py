from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import CommunityPost, PostLike, PostComment
from .serializers import CommunityPostSerializer, PostCommentSerializer


# ==================================================
# 📂 1. 카테고리별 게시글 목록 조회 (새로 추가)
# ==================================================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def community_list_by_category(request, category):
    """
    URL 파라미터로 받은 category를 대문자로 변환하여 해당 글만 필터링합니다.
    예: /api/community/category/free/ -> category='FREE' 글만 반환
    """
    category_upper = category.upper()
    posts = CommunityPost.objects.filter(category=category_upper).order_by("-created_at")
    
    # context에 request를 넘겨야 Serializer에서 is_liked 계산이 가능합니다.
    serializer = CommunityPostSerializer(posts, many=True, context={"request": request})
    return Response(serializer.data)


# ==================================================
# 📌 2. 게시글 목록(전체) + 생성
# ==================================================
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def post_list_create(request):
    if request.method == "GET":
        posts = CommunityPost.objects.all().order_by("-created_at")
        serializer = CommunityPostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)

    if request.method == "POST":
        serializer = CommunityPostSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            # author는 현재 로그인된 유저로 자동 저장 (Serializer logic에 따라)
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==================================================
# 📌 3. 게시글 상세 / 수정 / 삭제
# ==================================================
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def post_detail(request, post_id):
    post = get_object_or_404(CommunityPost, id=post_id)

    if request.method == "GET":
        serializer = CommunityPostSerializer(post, context={"request": request})
        return Response(serializer.data)

    if request.method == "PUT":
        if post.author != request.user:
            return Response({"detail": "권한 없음"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommunityPostSerializer(
            post,
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        if post.author != request.user:
            return Response({"detail": "권한 없음"}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================================================
# 👍 4. 좋아요 토글
# ==================================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_like(request, post_id):
    post = get_object_or_404(CommunityPost, id=post_id)

    like, created = PostLike.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()
        return Response({"liked": False})

    return Response({"liked": True})


# ==================================================
# 💬 5. 댓글 목록 + 생성
# ==================================================
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def comment_list_create(request, post_id):
    post = get_object_or_404(CommunityPost, id=post_id)

    if request.method == "GET":
        comments = post.comments.all().order_by("-created_at")
        serializer = PostCommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == "POST":
        serializer = PostCommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==================================================
# 💬 6. 댓글 삭제
# ==================================================
@api_view(['PUT', 'PATCH', 'DELETE']) # ✅ 사용할 메서드를 모두 등록
@permission_classes([IsAuthenticated])
def comment_update_delete(request, pk):
    comment = get_object_or_404(PostComment, pk=pk)

    # 1. 삭제 로직
    if request.method == 'DELETE':
        if comment.author != request.user:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # 2. 수정 로직 (PUT/PATCH)
    elif request.method in ['PUT', 'PATCH']:
        if comment.author != request.user:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = PostCommentSerializer(
            comment, 
            data=request.data, 
            partial=True, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_comments_list(request):
    # 로그인한 유저가 쓴 댓글만 필터링해서 가져옴
    comments = PostComment.objects.filter(author=request.user).order_by('-created_at')
    serializer = PostCommentSerializer(comments, many=True, context={'request': request})
    return Response(serializer.data)