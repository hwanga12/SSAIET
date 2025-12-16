import json
import requests

from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Meal, Food, MealFood, UserSelectedMeal, DinnerRecommendation
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

User = get_user_model()

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
        meal_data = meals[idx]  # meals: API에서 받아온 원본 메뉴 데이터

         # nutritionData로 p-score 계산
        p_score = calculate_p_score(result["nutritionData"])

        meal = Meal.objects.create(
            date=meal_data["date"],
            meal_time=meal_data["mealTimeId"],
            restaurant=meal_data["restaurantData"]["name"],
            course_type=meal_data["menuCourseName"][0],
            meal_name=result["mealName"],
            subMenuTxt=meal_data["subMenuTxt"],
            p_score=p_score
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


def calculate_p_score(nutrition_list):
    kcal = sum(n["calorie"] for n in nutrition_list)
    protein = sum(n["protein"] for n in nutrition_list)
    fat = sum(n["fat"] for n in nutrition_list)
    carbs = sum(n["carbohydrate"] for n in nutrition_list)

    score = 0
    if 500 <= kcal <= 800:
        score += 40
    else:
        score += max(5, 40 - abs(650 - kcal) * 0.1)

    ratio = protein / (carbs + fat + 1)
    if 0.25 <= ratio <= 0.4:
        score += 40

    if fat < 20:
        score += 20

    return round(score, 1)



## 유저 있는 테스트 버전
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommend_dinner(request):
    user = request.user
    usm_id = request.data.get("user_selected_meal_id")

    user_selected_meal = UserSelectedMeal.objects.get(
        id=usm_id,
        user=user
    )

    lunch = user_selected_meal.meal

    # 영양성분 합계
    foods = lunch.mealfood_set.select_related("food")
    total_nutrition = {
        "calorie": sum(f.food.calorie for f in foods),
        "carbs": sum(f.food.carbohydrate for f in foods),
        "protein": sum(f.food.protein for f in foods),
        "fat": sum(f.food.fat for f in foods),
    }

    # GPT에 넘길 prompt
    prompt = f"""
당신은 개인 맞춤 식단 전문가입니다.

[사용자 정보]
- 키: {user.height}
- 몸무게: {user.current_weight}
- 알러지: {user.allergies}
- 목표 체중: {user.target_weight}
- 근육량: {user.muscle_mass}
- 피트: {user.body_fat}
- 나이: {user.age}
- 성별: {user.gender}

[사용자가 선택한 점심]
- 선택 시각: {user_selected_meal.selected_at}
- 메뉴명: {lunch.meal_name}
- 구성: {lunch.subMenuTxt}
- P-Score: {lunch.p_score}

[점심 영양 성분]
- 칼로리: {total_nutrition['calorie']}
- 탄수화물: {total_nutrition['carbs']}
- 단백질: {total_nutrition['protein']}
- 지방: {total_nutrition['fat']}

위 정보를 고려하여 그날 그날 다르게 **저녁 식단 1개를 추천**하고,
왜 그 메뉴를 추천하는지 점심 식단과 사용자 정보를 고려하여 상세히 설명해주세요.

응답 형식:
{{
  "menu": "추천 저녁 메뉴 한 줄",
  "reason": "추천 이유"
}}
"""

    url = "https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions"

    body = {
        "model": "gpt-5-nano",
        "messages": [
            {"role": "developer", "content": "Answer in Korean"},
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.GMS_KEY}"
    }

    gpt_res = requests.post(url, json=body, headers=headers).json()
    ai_raw = gpt_res["choices"][0]["message"]["content"]

    ai_json = json.loads(ai_raw)

    # DB 저장
    dinner = DinnerRecommendation.objects.create(
        user=user,
        user_selected_meal=user_selected_meal,
        ai_menu_name=ai_json["menu"],
        ai_reason_text=ai_json["reason"],
        ai_response_json=json.dumps(ai_json),
        p_score=lunch.p_score
    )

    return JsonResponse({
        "success": True,
        "dinner_id": dinner.id,
        "ai_menu": ai_json["menu"],
        "reason": ai_json["reason"]
    })



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def select_meal(request):
    user = request.user
    meal_id = request.data.get("meal_id")

    if not meal_id:
        return Response({"error": "meal_id required"}, status=400)

    meal = Meal.objects.get(id=meal_id)

    usm = UserSelectedMeal.objects.create(
        user=user,
        meal=meal
    )

    return Response({
        "success": True,
        "user_selected_meal_id": usm.id
    })



# @csrf_exempt
# def recommend_dinner(request):

#     data = json.loads(request.body or "{}")
#     selected_meal_id = data["meal_id"]

#     lunch = Meal.objects.get(id=selected_meal_id)

#     foods = lunch.mealfood_set.select_related("food")
#     total_nutrition = {
#         "calorie": sum(f.food.calorie for f in foods),
#         "carbs": sum(f.food.carbohydrate for f in foods),
#         "protein": sum(f.food.protein for f in foods),
#         "fat": sum(f.food.fat for f in foods),
#     }

#     prompt = f"""
# 다음 점심에 기반하여 저녁 메뉴 1개를 추천하고 이유를 설명해줘.

# [점심]
# - 메뉴명: {lunch.meal_name}
# - 구성: {lunch.subMenuTxt}
# - P-Score: {lunch.p_score}

# [영양성분]
# - 칼로리: {total_nutrition['calorie']}
# - 탄수화물: {total_nutrition['carbs']}
# - 단백질: {total_nutrition['protein']}
# - 지방: {total_nutrition['fat']}

# JSON으로 응답:

# {{
#   "menu": "추천 메뉴",
#   "reason": "추천 이유"
# }}
# """

#     url = "https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions"

#     body = {
#         "model": "gpt-5-nano",
#         "messages": [
#             {"role": "developer", "content": "Answer in Korean"},
#             {"role": "user", "content": prompt}
#         ]
#     }

#     headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {settings.GMS_KEY}"
#     }

#     gpt_res = requests.post(url, json=body, headers=headers).json()
#     ai_raw = gpt_res["choices"][0]["message"]["content"]
#     ai_json = json.loads(ai_raw)

#     dinner = DinnerRecommendation.objects.create(
#         selected_lunch=lunch,
#         ai_menu_name=ai_json.get("menu"),
#         ai_reason_text=ai_json.get("reason"),
#         ai_response_json=json.dumps(ai_json),
#         p_score=lunch.p_score
#     )

#     return JsonResponse({
#         "success": True,
#         "dinner_id": dinner.id,
#         "menu": ai_json["menu"],
#         "reason": ai_json["reason"]
#     })
