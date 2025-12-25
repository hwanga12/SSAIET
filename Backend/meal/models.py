from django.db import models
from django.conf import settings

# models.py
class Meal(models.Model):
    date = models.IntegerField()
    meal_time = models.CharField(max_length=10)
    restaurant = models.CharField(max_length=100)
    course_type = models.CharField(max_length=10)   # A:한식, B:일품
    meal_name = models.CharField(max_length=200)
    subMenuTxt = models.TextField(null=True, blank=True)
    p_score = models.IntegerField(default=0)
    photoUrl = models.URLField(null=True, blank=True)



    def __str__(self):
        return f"{self.date} {self.course_type}"


class Food(models.Model):
    name = models.CharField(max_length=200, unique=True)
    calorie = models.IntegerField()
    carbohydrate = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    sugar = models.IntegerField()
    fiber = models.IntegerField()

    def __str__(self):
        return self.name


class MealFood(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    is_main = models.BooleanField()

    class Meta:
        unique_together = ('meal', 'food')


class UserSelectedMeal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    selected_at = models.DateTimeField(auto_now_add=True)


class DinnerRecommendation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date = models.IntegerField()
    user_selected_meal = models.ForeignKey(
        UserSelectedMeal,
        on_delete=models.CASCADE,
        related_name="dinner_recommendations"
    )

    ai_menu_name = models.CharField(max_length=255, null=True, blank=True)
    ai_reason_text = models.TextField(null=True, blank=True)
    ai_response_json = models.TextField(null=True, blank=True)
    p_score = models.FloatField(default=0)
    is_eaten = models.BooleanField(
        null=True,
        default=None,
        help_text="None: 미선택 / True: 먹음 / False: 안 먹음"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_dinner_per_lunch"
            )
        ]


class WeightChangePrediction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.IntegerField()
    predicted_weight_change = models.FloatField()
    progress_to_target = models.FloatField()
    estimated_weight = models.FloatField()
    progress_to_target = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
