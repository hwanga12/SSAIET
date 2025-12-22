from rest_framework import serializers
from .models import (
    CommunityPost,
    RestaurantRecommendation,
    ChangeReview,
    Question,
    PostLike,
    PostComment
)

# 🍽️ 식당 추천 Serializer
class RestaurantRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantRecommendation
        fields = ["restaurant_name", "location", "recommended_menu", "health_tag"]

# 📈 변화 후기 Serializer
class ChangeReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeReview
        fields = ["period", "change_type", "weight_diff"]

# ❓ Q&A Serializer
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["is_answered"]

# 🧩 커뮤니티 게시글 Serializer (핵심)
class CommunityPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)
    
    # 👍 좋아요 관련 필드 선언
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_mine = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    # 🔽 카테고리별 Nested 데이터
    restaurant_info = RestaurantRecommendationSerializer(required=False)
    review_info = ChangeReviewSerializer(required=False)
    question_info = QuestionSerializer(required=False)

    class Meta:
        model = CommunityPost
        fields = [
            "id", "author", "author_name", "category", "title", "content",
            "restaurant_info", "review_info", "question_info",
            "likes_count", "is_liked", "created_at", "updated_at",
            "is_mine", "comments_count"
        ]
        read_only_fields = ["author"]

    # 👍 좋아요 개수 계산
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count() # 게시글에 달린 댓글 수 반환
    
    # ❤️ 현재 유저가 좋아요를 눌렀는지 여부
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    # 내 글인지 확인하는 로직
    def get_is_mine(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False
    
    # ✍️ 게시글 생성 로직
   # community/serializers.py 의 create 메서드 부분

    def create(self, validated_data):
        # 1. 딕셔너리 데이터들을 validated_data에서 완전히 꺼냅니다 (pop)
        # 이렇게 해야 CommunityPost.objects.create 할 때 에러가 안 납니다.
        restaurant_data = validated_data.pop('restaurant_info', None)
        review_data = validated_data.pop('review_info', None)
        
        # 2. 메인 게시글 생성 (이제 validated_data 안에는 순수 Post 정보만 남음)
        post = CommunityPost.objects.create(**validated_data)
        
        # 3. 카테고리에 맞춰 하위 모델을 '따로' 생성하여 연결
        if post.category == 'RESTAURANT' and restaurant_data:
            from .models import RestaurantRecommendation
            RestaurantRecommendation.objects.create(post=post, **restaurant_data)
            
        elif post.category == 'REVIEW' and review_data:
            from .models import ChangeReview
            ChangeReview.objects.create(post=post, **review_data)
            
        return post

    # ✏️ 게시글 수정 로직
    def update(self, instance, validated_data):
        restaurant_data = validated_data.pop("restaurant_info", None)
        review_data = validated_data.pop("review_info", None)
        question_data = validated_data.pop("question_info", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if instance.category == "RESTAURANT" and restaurant_data:
            RestaurantRecommendation.objects.update_or_create(post=instance, defaults=restaurant_data)
        elif instance.category == "REVIEW" and review_data:
            ChangeReview.objects.update_or_create(post=instance, defaults=review_data)
        elif instance.category == "QNA" and question_data is not None:
            Question.objects.update_or_create(post=instance, defaults=question_data)
        return instance

class PostCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)
    is_mine = serializers.SerializerMethodField()
    
    # ✅ 내가 댓글을 단 '원본 글'의 제목과 ID, 카테고리를 가져옵니다.
    post_id = serializers.ReadOnlyField(source='post.id')
    post_title = serializers.ReadOnlyField(source='post.title')
    post_category = serializers.ReadOnlyField(source='post.category')

    class Meta:
        model = PostComment
        fields = [
            "id", "author_name", "content", "created_at", "is_mine",
            "post_id", "post_title", "post_category"  # ✅ 이 정보들이 있어야 목록에 보여줍니다.
        ]
        read_only_fields = ["author", "created_at"]
        
    def get_is_mine(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False