# meal/ml/inference.py
import torch
import joblib
import numpy as np
from meal.ml.model import WeightChangePredictor

from django.conf import settings
import os

INPUT_SIZE = 9

MODEL_PATH = os.path.join(settings.BASE_DIR, "meal/ml/weight_model.pt")
SCALER_PATH = os.path.join(settings.BASE_DIR, "meal/ml/scaler.pkl")

_model = None
_scaler = None

def load_model():
    global _model, _scaler
    if _model is None:
        _model = WeightChangePredictor(INPUT_SIZE)
        _model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
        _model.eval()
        _scaler = joblib.load(SCALER_PATH)

def predict_weight_change(feature_list):
    load_model()

    x = np.array([feature_list])
    x_scaled = _scaler.transform(x)
    x_tensor = torch.tensor(x_scaled, dtype=torch.float32)

    with torch.no_grad():
        pred = _model(x_tensor)

    return float(pred.item())
