from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random

# community
from community.models import CommunityPost, PostComment, PostLike

# meal
from meal.models import (
    Meal,
    UserSelectedMeal,
    DinnerRecommendation,
    WeightChangePrediction
)

User = get_user_model()


class Command(BaseCommand):
    help = "시연용 전체 더미 데이터 (유저 + 커뮤니티 + 식단 + 먹었어요 + 체중예측)"

    def handle(self, *args, **options):
        self.stdout.write("🚀 시연용 더미 데이터 생성 시작")

        # ==================================================
        # 1️⃣ 유저 5명 생성
        # ==================================================
        users = []
        for i in range(1, 6):
            user, created = User.objects.get_or_create(
                username=f"demo{i}",
                defaults={
                    "name": f"시연유저{i}",
                    "height": random.uniform(165, 180),
                    "current_weight": random.uniform(70, 85),
                    "target_weight": random.uniform(60, 72),
                    "muscle_mass": random.uniform(28, 38),
                    "body_fat": random.uniform(18, 28),
                    "age": random.randint(22, 35),
                    "gender": random.choice(["M", "F"]),
                }
            )
            if created:
                user.set_password("1234")
                user.save()
            users.append(user)

        self.stdout.write(self.style.SUCCESS("✔ 유저 5명 생성 완료 (demo1~5 / 비번 1234)"))

        # ==================================================
        # 2️⃣ 점심(Meal) 더미 생성
        # ==================================================
        meals = []
        today_int = int(datetime.today().strftime("%Y%m%d"))

        for i in range(10):
            meal = Meal.objects.create(
                date=today_int,
                meal_time="LUNCH",
                restaurant="SSAFY 식당",
                course_type=random.choice(["A", "B"]),
                meal_name=f"시연 점심 메뉴 {i+1}",
                subMenuTxt="시연용 서브 메뉴",
                p_score=random.randint(60, 95)
            )
            meals.append(meal)

        # ==================================================
        # 3️⃣ 유저 점심 선택 + 저녁 GPT 추천 + 먹었어요
        # ==================================================
        for user in users:
            base_weight = user.current_weight or 75.0

            for d in range(30):
                date = int((datetime.today() - timedelta(days=d)).strftime("%Y%m%d"))

                # 3-1) 점심 선택
                selected_meal = UserSelectedMeal.objects.create(
                    user=user,
                    meal=random.choice(meals)
                )

                # 3-2) GPT 저녁 추천 (흉내)
                eaten = random.choice([True, False])

                DinnerRecommendation.objects.create(
                    user=user,
                    date=date,
                    user_selected_meal=selected_meal,
                    ai_menu_name="🥗 고단백 닭가슴살 샐러드",
                    ai_reason_text="점심 영양 밸런스를 고려한 저녁 추천입니다.",
                    p_score=random.uniform(70, 95),
                    is_eaten=eaten
                )

                # 3-3) 체중 예측 결과
                if eaten:
                    base_weight -= random.uniform(0.05, 0.15)
                else:
                    base_weight += random.uniform(0.0, 0.1)

                WeightChangePrediction.objects.create(
                    user=user,
                    date=date,
                    predicted_weight_change=round(base_weight - user.current_weight, 2),
                    estimated_weight=round(base_weight, 1),
                    progress_to_target=round(
                        max(0, min(100,
                            (user.current_weight - base_weight)
                            / (user.current_weight - user.target_weight) * 100
                        )),
                        1
                    )
                )

        self.stdout.write(self.style.SUCCESS("✔ 식단 / 먹었어요 / 체중예측 생성 완료"))

        # ==================================================
        # 4️⃣ 커뮤니티 더미
        # ==================================================
        posts = []
        categories = ["FREE", "REVIEW", "QNA", "RESTAURANT"]

        for user in users:
            for i in range(3):
                post = CommunityPost.objects.create(
                    author=user,
                    category=random.choice(categories),
                    title=f"{user.name}의 시연 게시글 {i+1}",
                    content="시연을 위한 커뮤니티 더미 게시글입니다."
                )
                posts.append(post)

        for post in posts:
            for commenter in random.sample(users, k=random.randint(1, 3)):
                PostComment.objects.create(
                    post=post,
                    author=commenter,
                    content="시연용 댓글 👍"
                )

            for liker in random.sample(users, k=random.randint(0, 4)):
                PostLike.objects.get_or_create(
                    post=post,
                    user=liker
                )

        self.stdout.write(self.style.SUCCESS("✔ 커뮤니티 데이터 생성 완료"))
        self.stdout.write(self.style.SUCCESS("🎉 시연용 전체 더미 데이터 생성 완료!"))
