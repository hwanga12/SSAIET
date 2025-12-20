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
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

@csrf_exempt
def save_meal_data(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    data = json.loads(request.body or "{}")

    date_value = data.get("date", date.today().strftime("%Y%m%d"))
    meal_time_id = data.get("mealTimeId", "2")

    # =========================
    # 1. DB에 없으면 외부 API 호출 + 저장
    # =========================
    if not Meal.objects.filter(date=date_value, meal_time=meal_time_id).exists():

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

        # 🔥 DB 저장
        for result in nutrition_res["results"]:

            if not result.get("success"):
                continue

            idx = result["mealIndex"]
            meal_data = meals[idx]

            p_score = calculate_p_score(result["nutritionData"])

            meal = Meal.objects.create(
                date=meal_data["date"],
                meal_time=meal_data["mealTimeId"],
                restaurant=meal_data["restaurantData"]["name"],
                course_type=meal_data["menuCourseName"][0],
                meal_name=result["mealName"],
                subMenuTxt=meal_data["subMenuTxt"],
                photoUrl=meal_data["photoUrl"],
                p_score=p_score
            )

            for food_data in result["nutritionData"]:
                food, _ = Food.objects.get_or_create(
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

    # =========================
    # 2. 🔥 항상 여기서 DB 조회 후 응답
    # =========================
    meals = Meal.objects.filter(
        date=date_value,
        meal_time=meal_time_id
    )

    result = []
    for meal in meals:
        foods = meal.mealfood_set.select_related("food")
        result.append({
             "id": meal.id,   
            "meal_name": meal.meal_name,
            "course_type": meal.course_type,
            "subMenuTxt": meal.subMenuTxt,
            "photoUrl": meal.photoUrl,
            "p_score": meal.p_score,
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
        "date": date_value,
        "mealTimeId": meal_time_id,
        "data": result
    })

def calculate_p_score(nutrition_list):
    kcal = sum(n["calorie"] for n in nutrition_list)
    protein = sum(n["protein"] for n in nutrition_list)
    fat = sum(n["fat"] for n in nutrition_list)
    carbs = sum(n["carbohydrate"] for n in nutrition_list)

    score = 0

    # 1️⃣ 칼로리 점수 (0~35)
    ideal_kcal = 650
    kcal_diff = abs(kcal - ideal_kcal)
    kcal_score = max(0, 35 - (kcal_diff / 10))
    score += kcal_score

    # 2️⃣ 단백질 비율 점수 (0~40)
    ratio = protein / (protein + carbs + fat + 1)

    if ratio < 0.15:
        protein_score = ratio / 0.15 * 20
    elif ratio <= 0.35:
        protein_score = 20 + (ratio - 0.15) / 0.2 * 20
    else:
        protein_score = max(20, 40 - (ratio - 0.35) * 100)

    score += protein_score

    # 3️⃣ 지방 점수 (0~25)
    if fat <= 15:
        fat_score = 25
    elif fat <= 30:
        fat_score = 25 - (fat - 15) * 1.2
    else:
        fat_score = max(5, 25 - (fat - 15) * 2)

    score += fat_score

    return round(score, 1)




## 유저 있는 테스트 버전
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
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
@authentication_classes([JWTAuthentication])
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
