# meal/ml/train.py
import os
import sys
import django
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ssaiet.settings")
django.setup()

import pandas as pd
import torch
import joblib
import torch.nn as nn
import torch.optim as optim

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from meal.models import MealFood, DinnerRecommendation
from django.contrib.auth import get_user_model
from meal.ml.model import WeightChangePredictor

User = get_user_model()

RECOMMENDED_DINNER_CAL = 600  # ⭐ 안 먹은 날 가정 칼로리


def get_data_from_db():
    rows = []

    for user in User.objects.all():
        today = pd.Timestamp.today().normalize()
        start = today - pd.Timedelta(days=30)

        # 날짜별 기본값 (안 먹은 날)
        daily_calories = {
            (start + pd.Timedelta(days=i)).date(): RECOMMENDED_DINNER_CAL
            for i in range(30)
        }

        dinners = DinnerRecommendation.objects.filter(
            user=user,
            created_at__date__gte=start.date(),
            is_eaten=True
        ).select_related("user_selected_meal__meal")

        for d in dinners:
            meal = d.user_selected_meal.meal
            calories = sum(
                mf.food.calorie
                for mf in MealFood.objects.filter(meal=meal).select_related("food")
            )
            daily_calories[d.created_at.date()] = calories

        avg_calories = sum(daily_calories.values()) / 30

        rows.append({
            "age": user.age,
            "gender": 1 if user.gender == "M" else 0,
            "height": user.height,
            "current_weight": user.current_weight,
            "target_weight": user.target_weight,
            "muscle_mass": user.muscle_mass,
            "body_fat": user.body_fat,
            "avg_calories": avg_calories,
            "meal_count": 30,
            # ⭐ 하루 체중 변화량 (라벨)
            "weight_change": (user.target_weight - user.current_weight) / 90
        })

    return pd.DataFrame(rows)


df = get_data_from_db()

X = df.drop(columns=["weight_change"])
y = df["weight_change"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)



X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
y_tensor = torch.tensor(y.values, dtype=torch.float32).view(-1, 1)

model = WeightChangePredictor(input_size=X_tensor.shape[1])
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    optimizer.zero_grad()
    preds = model(X_tensor)
    loss = criterion(preds, y_tensor)
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f"[Epoch {epoch}] Loss: {loss.item():.4f}")

torch.save(model.state_dict(), "meal/ml/weight_model.pt")
joblib.dump(scaler, "meal/ml/scaler.pkl")

print("✅ 학습 완료 (최근 30일 기준)")
