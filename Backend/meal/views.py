import json
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from meal.ml.inference import predict_weight_change

from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Meal, Food, MealFood, UserSelectedMeal, DinnerRecommendation, WeightChangePrediction
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models import Sum


User = get_user_model()

@csrf_exempt
def save_meal_data(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    data = json.loads(request.body or "{}")

    date_value = int(data.get("date", date.today().strftime("%Y%m%d")))
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



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def recommend_dinner(request):
    user = request.user

    # =========================
    # CASE 1️⃣ 날짜로 기존 저녁 조회 (달력 이동 / 최초 진입)
    # =========================
    date_value = request.data.get("date")
    if date_value:
        existing = DinnerRecommendation.objects.filter(
            user=user,
            date=date_value
        ).first()

        if existing:
            return JsonResponse({
                "success": True,
                "cached": True,
                "dinner_id": existing.id,
                "ai_menu": existing.ai_menu_name,
                "reason": existing.ai_reason_text,
                "is_eaten": existing.is_eaten,
            })

        return JsonResponse({
            "success": True,
            "cached": False,
        })

    # =========================
    # CASE 2️⃣ 점심 선택 후 저녁 추천
    # =========================
    usm_id = request.data.get("user_selected_meal_id")
    if not usm_id:
        return Response(
            {"error": "date or user_selected_meal_id required"},
            status=400
        )

    user_selected_meal = UserSelectedMeal.objects.filter(
        id=usm_id,
        user=user
    ).select_related("meal").first()

    if not user_selected_meal:
        return Response(
            {"error": "UserSelectedMeal not found"},
            status=404
        )

    lunch = user_selected_meal.meal
    date_value = lunch.date

    # 🔥 이미 그 날짜에 저녁 추천이 있으면 그대로 반환
    existing = DinnerRecommendation.objects.filter(
        user=user,
        date=date_value
    ).first()

    if existing:
        return JsonResponse({
            "success": True,
            "cached": True,
            "dinner_id": existing.id,
            "ai_menu": existing.ai_menu_name,
            "reason": existing.ai_reason_text,
            "is_eaten": existing.is_eaten,
        })

    # =========================
    # GPT 추천 생성
    # =========================
    foods = lunch.mealfood_set.select_related("food")
    total_nutrition = {
        "calorie": sum(f.food.calorie for f in foods),
        "carbs": sum(f.food.carbohydrate for f in foods),
        "protein": sum(f.food.protein for f in foods),
        "fat": sum(f.food.fat for f in foods),
    }

    prompt = f"""
당신은 개인 맞춤 식단 전문가입니다.

[사용자 정보]
- 키: {user.height}
- 몸무게: {user.current_weight}
- 알러지: {user.allergies}
- 목표 체중: {user.target_weight}
- 근육량: {user.muscle_mass}
- 체지방률: {user.body_fat}
- 나이: {user.age}
- 성별: {user.gender}

[점심 식단]
- 메뉴명: {lunch.meal_name}
- 구성: {lunch.subMenuTxt}
- P-Score: {lunch.p_score}

[점심 영양]
- 칼로리: {total_nutrition['calorie']}
- 탄수화물: {total_nutrition['carbs']}
- 단백질: {total_nutrition['protein']}
- 지방: {total_nutrition['fat']}

    위 정보를 기반으로 **오늘 하루에 맞는 저녁 식사 1개만 추천**하세요.
    너무 자세한 g은 빼주고, 마지막에 반드시 '총 칼로리: [숫자]kcal' 형식으로 적어주세요.


응답 형식(JSON):
{{
  "menu": "추천 저녁 메뉴",
  "reason": "추천 이유"
}}
"""

    url = "https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions"
    body = {
        "model": "gpt-5.2",
        "messages": [
            {"role": "developer", "content": "Answer in Korean"},
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {settings.GMS_KEY}",
        "Content-Type": "application/json"
    }

    gpt_res = requests.post(url, json=body, headers=headers).json()
    ai_json = json.loads(gpt_res["choices"][0]["message"]["content"])

    dinner = DinnerRecommendation.objects.create(
        user=user,
        user_selected_meal=user_selected_meal,
        date=date_value,
        ai_menu_name=ai_json["menu"],
        ai_reason_text=ai_json["reason"],
        ai_response_json=json.dumps(ai_json),
        p_score=lunch.p_score,
    )

    return JsonResponse({
        "success": True,
        "cached": False,
        "dinner_id": dinner.id,
        "ai_menu": dinner.ai_menu_name,
        "reason": dinner.ai_reason_text,
        "is_eaten": dinner.is_eaten,
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_dinner_status(request):
    dinner_id = request.data.get("dinner_id")
    is_eaten = request.data.get("is_eaten")

    dinner = DinnerRecommendation.objects.get(
        id=dinner_id,
        user=request.user
    )

    dinner.is_eaten = is_eaten
    dinner.save()

    return Response({
        "success": True,
        "is_eaten": dinner.is_eaten
    })

from datetime import date
from calendar import monthrange
from .serializers import CalendarDaySerializer,NutritionDayDetailSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def nutrition_calendar_month(request):
    """
    📅 월 캘린더 조회 API
    - 점심: 사용자가 선택한 메뉴 (요약)
    - 저녁: AI 추천 결과 + 섭취 여부
    """
    user = request.user

    year = int(request.GET.get("year"))
    month = int(request.GET.get("month"))

    # 해당 월 시작 / 끝
    start_date = year * 10000 + month * 100 + 1
    end_day = monthrange(year, month)[1]
    end_date = year * 10000 + month * 100 + end_day

    # ===============================
    # 1️⃣ 점심 (UserSelectedMeal)
    # ===============================
    lunch_qs = (
        UserSelectedMeal.objects
        .select_related("meal")
        .filter(
            user=user,
            meal__date__range=[start_date, end_date]
        )
    )

    # date(int) 기준으로 매핑
    lunch_map = {
        usm.meal.date: usm
        for usm in lunch_qs
    }

    # ===============================
    # 2️⃣ 저녁 (DinnerRecommendation)
    # ===============================
    dinner_qs = DinnerRecommendation.objects.filter(
        user=user,
        date__range=[start_date, end_date]
    )

    dinner_map = {
        dr.date: dr
        for dr in dinner_qs
    }

    # ===============================
    # 3️⃣ 날짜별 데이터 조합
    # ===============================
    result = []

    for day in range(1, end_day + 1):
        current_date = year * 10000 + month * 100 + day

        lunch = lunch_map.get(current_date)
        dinner = dinner_map.get(current_date)

        # 아무 기록도 없는 날은 제외 (원하면 제거 가능)
        if not lunch and not dinner:
            continue

        result.append({
            "date": current_date,
            "lunch": {
                "meal_name": lunch.meal.meal_name,
                "course_type": lunch.meal.course_type,
            } if lunch else None,
            "dinner": {
                "ai_menu_name": dinner.ai_menu_name,
                "is_eaten": dinner.is_eaten,
            } if dinner else None,
        })

    # ===============================
    # 4️⃣ Serializer로 포장
    # ===============================
    serializer = CalendarDaySerializer(result, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def nutrition_day_detail(request, date):
    """
    📄 날짜 상세 조회 API
    - 해당 날짜의 점심 + 저녁 전체 정보
    - 캘린더에서 날짜 클릭 시 사용
    """
    user = request.user

    # ===============================
    # 1️⃣ 점심 (UserSelectedMeal → Meal)
    # ===============================
    lunch_obj = (
        UserSelectedMeal.objects
        .select_related("meal")
        .filter(user=user, meal__date=date)
        .first()
    )

    lunch_data = None
    if lunch_obj:
        meal = lunch_obj.meal
        lunch_data = {
            "meal_name": meal.meal_name,
            "course_type": meal.course_type,
            "restaurant": meal.restaurant,
            "subMenuTxt": meal.subMenuTxt,
            "p_score": meal.p_score,
            "photoUrl": meal.photoUrl,
        }

    # ===============================
    # 2️⃣ 저녁 (DinnerRecommendation)
    # ===============================
    dinner_obj = DinnerRecommendation.objects.filter(
        user=user,
        date=date
    ).first()

    dinner_data = None
    if dinner_obj:
        dinner_data = {
            "ai_menu_name": dinner_obj.ai_menu_name,
            "ai_reason_text": dinner_obj.ai_reason_text,
            "p_score": dinner_obj.p_score,
            "is_eaten": dinner_obj.is_eaten,
        }

    # ===============================
    # 3️⃣ 응답 조합
    # ===============================
    result = {
        "date": date,
        "lunch": lunch_data,
        "dinner": dinner_data,
    }

    serializer = NutritionDayDetailSerializer(result)
    return Response(serializer.data)

import torch

RECOMMENDED_DINNER_CAL = 600  # 안 먹은 날 가정 칼로리

import re

# 텍스트에서 숫자만 추출하는 도우미 함수 (함수 밖이나 내부에 정의)
def extract_calories(text):
    if not text: return 600
    # '총 칼로리: 550' 또는 '550kcal' 등에서 숫자만 추출
    match = re.search(r'(\d+)\s*kcal|총\s*칼로리\s*[:\s]*(\d+)', text)
    if match:
        return int(match.group(1) or match.group(2))
    return 600

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def predict_weight_change_view(request):
    user = request.user
    today = datetime.now().date()
    start_date = today - timedelta(days=30)
    baseline_weight = user.current_weight

    # 1. 30일치 기본값 세팅 (데이터 없는 날은 1800kcal로 가정)
    daily_calories = { (start_date + timedelta(days=i)): 1800 for i in range(30) }

    # 2. 실제 기록(DinnerRecommendation) 가져오기
    dinners = DinnerRecommendation.objects.filter(
        user=user,
        created_at__date__gte=start_date
    ).select_related("user_selected_meal__meal")

    for dinner in dinners:
        date_key = dinner.created_at.date()
        day_total = 0
        
        # [점심] DB에서 실제 음식 칼로리 합산
        lunch_meal = dinner.user_selected_meal.meal
        lunch_cal = lunch_meal.mealfood_set.aggregate(
            total=Sum('food__calorie')
        )['total'] or 0
        day_total += lunch_cal

        # [저녁] GPT 응답 텍스트(ai_reason_text)에서 파싱
        # 사용자가 '먹었음' 체크를 안 했더라도 추천받은 시점의 칼로리를 일단 계산에 넣습니다.
        dinner_cal = extract_calories(dinner.ai_reason_text)
        day_total += dinner_cal

        # [아침/간식] 기록이 없으므로 가볍게 200~300kcal 추가 (선택 사항)
        day_total += 300 

        daily_calories[date_key] = day_total

    # 3. 평균 계산 및 모델 입력
    avg_calories = sum(daily_calories.values()) / 30

    # =========================
    # 6️⃣ ML 입력 (train.py와 동일)
    # =========================
    feature_list = [
        user.age,
        1 if user.gender == "M" else 0,
        user.height,
        baseline_weight,
        user.target_weight,
        user.muscle_mass,
        user.body_fat,
        avg_calories,
        30,  # 최근 30일
    ]

    # =========================
    # 7️⃣ ML 예측 (30일 후 변화량)
    # =========================
    predicted_delta_30d = predict_weight_change(feature_list)

    # ⭐ 현실성 클램프 (선택이지만 강력 추천)
    predicted_delta_30d = max(min(predicted_delta_30d, 5.0), -5.0)

    predicted_weight_30d = baseline_weight + predicted_delta_30d

    # =========================
    # 8️⃣ 진척도 계산 (핵심)
    # =========================
    if baseline_weight == user.target_weight:
        progress = 100.0
    else:
        progress = (
            (baseline_weight - predicted_weight_30d)
            / (baseline_weight - user.target_weight)
        ) * 100

    progress = max(0, min(progress, 100))

    # =========================
    # 9️⃣ 저장 (히스토리용)
    # =========================
    WeightChangePrediction.objects.create(
        user=user,
        date=int(today.strftime("%Y%m%d")),
        predicted_weight_change=predicted_delta_30d,
        estimated_weight=predicted_weight_30d,
        progress_to_target=progress,
    )

    # =========================
    # 🔟 응답
    # =========================
    
    return Response({
    "current_weight": round(baseline_weight, 1),
    "target_weight": round(user.target_weight, 1),
    "predicted_weight_30d": round(predicted_weight_30d, 1),
    "predicted_weight_change": round(predicted_delta_30d, 2),
    "progress_to_target": round(progress, 1),
})
