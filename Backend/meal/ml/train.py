# meal/ml/train.py 맨 위
import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ssaiet.settings")
django.setup()


import pandas as pd
import torch
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 🔥 Django 모델 import (이게 빠져서 터진 거임)
from meal.models import (
    Meal,
    Food,
    MealFood,
    UserSelectedMeal
)
from django.contrib.auth import get_user_model

User = get_user_model()

from meal.ml.model import WeightChangePredictor
import torch.nn as nn
import torch.optim as optim


# Django에서 데이터를 가져오는 함수 (기존 코드)
def get_data_from_db():
    data = []
    users = User.objects.all()

    for user in users:
        selected_meals = UserSelectedMeal.objects.filter(user=user)

        for selected_meal in selected_meals:
            meal = selected_meal.meal

            # MealFood 모델을 통해 식사에 포함된 음식을 가져오기
            total_calories = 0
            total_protein = 0
            total_carbs = 0
            total_fat = 0

            # MealFood 모델을 사용하여 해당 Meal에 포함된 모든 음식 가져오기
            meal_foods = MealFood.objects.filter(meal=meal)

            for mf in meal_foods:
                food = mf.food
                total_calories += food.calorie
                total_protein += food.protein
                total_carbs += food.carbohydrate
                total_fat += food.fat

            data.append({
                'age': user.age,
                'gender': 1 if user.gender == 'M' else 0,
                'height': user.height,
                'current_weight': user.current_weight,
                'target_weight': user.target_weight,
                'muscle_mass': user.muscle_mass,
                'body_fat': user.body_fat,
                'total_calories': total_calories,
                'total_protein': total_protein,
                'total_carbs': total_carbs,
                'total_fat': total_fat,
                'meal_count': selected_meals.count(),
                'weight_change': user.current_weight - user.target_weight
            })

    df = pd.DataFrame(data)
    return df


# 데이터 준비
df = get_data_from_db()

# 특성과 라벨 분리
X = df.drop(columns=['weight_change'])
y = df['weight_change']

# 데이터 표준화 (StandardScaler)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 학습용 데이터와 테스트용 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 데이터를 PyTorch 텐서로 변환
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)  # 1D 벡터로 변환

X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)

# 모델 초기화
model = WeightChangePredictor(input_size=X_train.shape[1])

# 손실 함수 및 옵티마이저 설정
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 모델 학습
num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()

    # 예측
    predictions = model(X_train_tensor)
    
    # 손실 계산
    loss = criterion(predictions, y_train_tensor)
    
    # 역전파 및 최적화
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f'Epoch [{epoch}/{num_epochs}], Loss: {loss.item()}')

# 새로운 데이터 예시
new_data = torch.tensor([[33, 1, 178, 80, 75, 35, 20, 2400, 110, 270, 80, 3]], dtype=torch.float32)

# 예측 수행
model.eval()  # 평가 모드로 설정
with torch.no_grad():  # 기울기 계산 비활성화
    prediction = model(new_data)
    print(f'Predicted Weight Change: {prediction.item()}')


torch.save(model.state_dict(), "meal/ml/weight_model.pt")

# 스케일러 저장 (중요)
joblib.dump(scaler, "meal/ml/scaler.pkl")

print("✅ 모델 학습 및 저장 완료")