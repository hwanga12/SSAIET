from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# ==================================================
# 🧩 1. 커뮤니티 공통 게시글
# ==================================================
class CommunityPost(models.Model):

    CATEGORY_CHOICES = [
        ("RESTAURANT", "식당 추천"),
        ("REVIEW", "변화 후기"),
        ("QNA", "Q&A"),
        ("FREE", "잡담"),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="community_posts"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )
    title = models.CharField(max_length=100)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.category}] {self.title}"


# ==================================================
# 🍽️ 2. 식당 추천 (Restaurant)
# ==================================================
class RestaurantRecommendation(models.Model):

    post = models.OneToOneField(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name="restaurant_info"
    )

    restaurant_name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    recommended_menu = models.CharField(max_length=100)

    HEALTH_TAG_CHOICES = [
        ("HIGH_PROTEIN", "고단백"),
        ("LOW_FAT", "저지방"),
        ("BALANCED", "균형식"),
        ("DIET", "다이어트"),
        ("OUT", "외식"),
    ]

    health_tag = models.CharField(
        max_length=20,
        choices=HEALTH_TAG_CHOICES
    )

    def __str__(self):
        return self.restaurant_name


# ==================================================
# 📈 3. 변화 후기 (Review)
# ==================================================
class ChangeReview(models.Model):

    post = models.OneToOneField(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name="review_info"
    )

    PERIOD_CHOICES = [
        ("1W", "1주"),
        ("2W", "2주"),
        ("1M", "1개월"),
    ]

    CHANGE_TYPE_CHOICES = [
        ("WEIGHT", "체중 변화"),
        ("DIET", "식습관 변화"),
        ("EXERCISE", "운동 습관"),
    ]

    period = models.CharField(
        max_length=2,
        choices=PERIOD_CHOICES
    )
    change_type = models.CharField(
        max_length=20,
        choices=CHANGE_TYPE_CHOICES
    )

    weight_diff = models.FloatField(
        null=True,
        blank=True,
        help_text="체중 변화 (kg, 감소는 음수)"
    )

    def __str__(self):
        return f"{self.period} 변화 후기"


# ==================================================
# ❓ 4. Q&A
# ==================================================
class Question(models.Model):

    post = models.OneToOneField(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name="question_info"
    )

    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return "Q&A"


# ==================================================
# 👍 5. 공감(Like)
# ==================================================
class PostLike(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user} likes {self.post.id}"

# ==================================================
# 💬 6. 댓글 (Comment) - 기존 models.py 맨 아래 추가
# ==================================================
class PostComment(models.Model):
    post = models.ForeignKey(
        CommunityPost, 
        on_delete=models.CASCADE, # 🔥 on_Harris 오타 수정
        related_name='comments'
    )
    author = models.ForeignKey(
        User,  # 상단에 선언하신 User 변수 그대로 사용
        on_delete=models.CASCADE,
        related_name="community_comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.content[:10]}"
