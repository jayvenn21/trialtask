# ml_predictor/utils.py
import joblib
from sklearn.linear_model import LinearRegression
from data_fetcher.models import StockData
import pandas as pd
import numpy as np

def train_and_save_model(symbol):
    data = StockData.objects.filter(symbol=symbol).order_by('date')
    df = pd.DataFrame(list(data.values()))

    X = df.index.values.reshape(-1, 1)
    y = df['close_price'].values

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, f'ml_predictor/models/{symbol}_model.pkl')

def predict_prices(symbol, days=30):
    model = joblib.load(f'ml_predictor/models/{symbol}_model.pkl')
    last_index = StockData.objects.filter(symbol=symbol).count()
    future_indices = np.arange(last_index, last_index + days).reshape(-1, 1)
    predictions = model.predict(future_indices)

    return predictions.tolist()