# meal/ml/train.py
import os
import sys
import django
import re
from datetime import timedelta

# 프로젝트 루트 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ssaiet.settings")
django.setup()

import pandas as pd
import torch
import joblib
import torch.nn as nn
import torch.optim as optim
from django.db.models import Sum
from sklearn.preprocessing import StandardScaler

from meal.models import MealFood, DinnerRecommendation
from django.contrib.auth import get_user_model
from meal.ml.model import WeightChangePredictor

User = get_user_model()

RECOMMENDED_DINNER_CAL = 600  # 기본 저녁 칼로리

# =========================
# 텍스트에서 칼로리 숫자 추출하는 함수
# =========================
def extract_calories(text):
    if not text:
        return RECOMMENDED_DINNER_CAL
    # "예상 칼로리: 550kcal" 또는 "550kcal" 패턴에서 숫자만 추출
    match = re.search(r'(\d+)\s*kcal|칼로리\s*[:\s]*(\d+)', text)
    if match:
        return int(match.group(1) or match.group(2))
    return RECOMMENDED_DINNER_CAL

def get_data_from_db():
    rows = []
    users = User.objects.all()
    
    if not users.exists():
        print("⚠️ DB에 사용자가 없습니다.")
        return pd.DataFrame()

    for user in users:
        print(f"\n--- [사용자 학습 데이터 추출: {user.username}] ---")
        today = pd.Timestamp.today().normalize()
        start = today - pd.Timedelta(days=30)

        # 기본 하루 권장량 1800 가정 (데이터가 아예 없는 날 대비)
        daily_total_calories = {
            (start + pd.Timedelta(days=i)).date(): 1800
            for i in range(30)
        }

        # 30일간의 기록 조회
        recommendations = DinnerRecommendation.objects.filter(
            user=user,
            created_at__date__gte=start.date()
        ).select_related("user_selected_meal__meal")

       # train.py 내의 루프 수정
    for rec in recommendations:
        date_key = rec.created_at.date()
        day_calories = 0
        
        # [A] 실제 먹은 점심 칼로리 계산 (수정된 방식)
        lunch_meal = rec.user_selected_meal.meal
        
        # 해당 Meal에 연결된 모든 Food의 calorie 합산
        # MealFood를 거쳐 Food 테이블의 calorie를 가져옵니다.
        lunch_cal = MealFood.objects.filter(meal=lunch_meal).aggregate(
            total=Sum('food__calorie')
        )['total'] or 0
        
        day_calories += lunch_cal

        # [B] GPT 응답 텍스트에서 저녁 칼로리 파싱
        dinner_cal = extract_calories(rec.ai_reason_text)
        day_calories += dinner_cal

        # [C] 보정치
        day_calories += 300

        daily_total_calories[date_key] = day_calories
        
        # 🔍 로그 출력 (이제 lunch_cal이 0이 아니어야 합니다)
        print(f"[{date_key}] 점심({lunch_meal.meal_name}): {lunch_cal}kcal + 저녁: {dinner_cal}kcal + 보정: 300kcal = 총 {day_calories}kcal")

        # 30일 평균 계산
        avg_daily_cal = sum(daily_total_calories.values()) / 30
        print(f">> 최근 30일 평균 섭취량: {avg_daily_cal:.2f}kcal")

        # BMR 및 체중 변화 예측 정답지 생성
        if user.gender == "M":
            bmr = (10 * user.current_weight) + (6.25 * user.height) - (5 * user.age) + 5
        else:
            bmr = (10 * user.current_weight) + (6.25 * user.height) - (5 * user.age) - 161
        
        tdee = bmr * 1.2
        daily_weight_change = (avg_daily_cal - tdee) / 7700

        rows.append({
            "age": user.age,
            "gender": 1 if user.gender == "M" else 0,
            "height": user.height,
            "current_weight": user.current_weight,
            "target_weight": user.target_weight,
            "muscle_mass": user.muscle_mass,
            "body_fat": user.body_fat,
            "avg_calories": avg_daily_cal, 
            "meal_count": 30,
            "weight_change": daily_weight_change
        })

    return pd.DataFrame(rows)

# =========================
# 메인 학습 프로세스
# =========================
print("🔄 데이터베이스 분석을 시작합니다...")
df = get_data_from_db()

if df.empty:
    print("❌ 학습할 데이터프레임이 비어있습니다. 데이터를 확인해 주세요.")
    sys.exit()

X = df.drop(columns=["weight_change"])
y = df["weight_change"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
y_tensor = torch.tensor(y.values, dtype=torch.float32).view(-1, 1)

model = WeightChangePredictor(input_size=X_tensor.shape[1])
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

print("\n🚀 모델 학습을 시작합니다...")
for epoch in range(101):
    optimizer.zero_grad()
    preds = model(X_tensor)
    loss = criterion(preds, y_tensor)
    loss.backward()
    optimizer.step()

    if epoch % 20 == 0:
        print(f"[Epoch {epoch:3d}/100] Loss: {loss.item():.8f}")

torch.save(model.state_dict(), "meal/ml/weight_model.pt")
joblib.dump(scaler, "meal/ml/scaler.pkl")

print("\n✅ 모든 과정이 완료되었습니다.")
print("- 모델 저장 경로: meal/ml/weight_model.pt")
print("- 스케일러 저장 경로: meal/ml/scaler.pkl")