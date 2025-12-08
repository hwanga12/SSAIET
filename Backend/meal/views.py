import json
import requests

from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Meal, Food, MealFood


@csrf_exempt
def save_meal_data(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    data = json.loads(request.body or "{}")

    # 날짜 없으면 오늘 날짜 자동 사용
    date_value = data.get("date", date.today().strftime("%Y%m%d"))
    meal_time_id = data.get("mealTimeId", "2")

    # =========================
    # 1. 이미 DB에 있다면 바로 반환
    # =========================
    if Meal.objects.filter(date=date_value, meal_time=meal_time_id).exists():

        meals = Meal.objects.filter(
            date=date_value,
            meal_time=meal_time_id
        )

        result = []
        for meal in meals:
            foods = meal.mealfood_set.select_related("food")
            result.append({
                "meal_name": meal.meal_name,
                "course_type": meal.course_type,
                "foods": [
                    {
                        "name": mf.food.name,
                        "calorie": mf.food.calorie,
                        "carbohydrate": mf.food.carbohydrate,
                        "protein": mf.food.protein,
                        "fat": mf.food.fat,
                        "sugar": mf.food.sugar,
                        "fiber": mf.food.fiber,
                        "is_main": mf.is_main
                    }
                    for mf in foods
                ]
            })

        return JsonResponse({
            "success": True,
            "source": "DB",
            "date": date_value,
            "mealTimeId": meal_time_id,
            "data": result
        })

    # =========================
    # 2. 없으면 외부 API 호출
    # =========================

    meals_url = "https://welplan.pmh.codes/api/restaurants/meals"

    body = {
        "restaurantData": {
            "id": "REST000133",
            "name": "멀티캠퍼스",
            "description": "멀티캠퍼스|SDS|삼성|에스디에스"
        },
        "date": date_value,
        "mealTimeId": meal_time_id,
        "sessionId": "default"
    }

    meal_res = requests.post(meals_url, json=body).json()

    if "meals" not in meal_res:
        return JsonResponse({"success": False, "error": "No meals data"}, status=400)

    # A/B 코스만 필터링
    meals = [
        m for m in meal_res["meals"]
        if m["menuCourseName"][0] in ["A", "B"]
    ]

    nutrition_url = "https://welplan.pmh.codes/api/meals/nutrition/bulk"
    nutrition_body = {
        "mealsData": meals,
        "sessionId": "default"
    }

    nutrition_res = requests.post(nutrition_url, json=nutrition_body).json()

    if "results" not in nutrition_res:
        return JsonResponse({"success": False, "error": "No nutrition results"}, status=400)

    save_count = 0

    # =========================
    # 3. DB 저장
    # =========================
    for result in nutrition_res["results"]:

        if not result.get("success"):
            continue

        idx = result["mealIndex"]
        meal_data = meals[idx]

        meal = Meal.objects.create(
            date=meal_data["date"],
            meal_time=meal_data["mealTimeId"],
            restaurant=meal_data["restaurantData"]["name"],
            course_type=meal_data["menuCourseName"][0],
            meal_name=result["mealName"],
        )

        for food_data in result["nutritionData"]:
            food, created = Food.objects.get_or_create(
                name=food_data["name"],
                defaults={
                    "calorie": food_data["calorie"],
                    "carbohydrate": food_data["carbohydrate"],
                    "protein": food_data["protein"],
                    "fat": food_data["fat"],
                    "sugar": food_data["sugar"],
                    "fiber": food_data["fiber"],
                }
            )

            MealFood.objects.create(
                meal=meal,
                food=food,
                is_main=food_data["isMain"]
            )

        save_count += 1

    return JsonResponse({
        "success": True,
        "source": "API",
        "saved_meals": save_count,
        "date": date_value,
        "mealTimeId": meal_time_id
    })
