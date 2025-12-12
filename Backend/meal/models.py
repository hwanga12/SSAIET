from django.db import models

# Create your models here.
# models.py
class Meal(models.Model):
    date = models.IntegerField()
    meal_time = models.CharField(max_length=10)
    restaurant = models.CharField(max_length=100)
    course_type = models.CharField(max_length=10)   # A:한식, B:일품
    meal_name = models.CharField(max_length=200)
    subMenuTxt = models.TextField(null=True, blank=True)
    p_score = models.IntegerField(default=0)



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
    # user = models.ForeignKey(User, on_delete=models.CASCADE)  # 일단 제거
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    selected_at = models.DateTimeField(auto_now_add=True)


class DinnerRecommendation(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)  # 일단 제거
    selected_lunch = models.ForeignKey(Meal, on_delete=models.CASCADE)

    ai_menu_name = models.CharField(max_length=255, null=True, blank=True)
    ai_reason_text = models.TextField(null=True, blank=True)
    ai_response_json = models.TextField(null=True, blank=True)
    p_score = models.FloatField(default=0)
