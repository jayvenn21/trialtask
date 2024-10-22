# data_fetcher/models.py
from django.db import models

class StockData(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('symbol', 'date')

# data_fetcher/utils.py
import requests
from datetime import datetime, timedelta
from .models import StockData

def fetch_stock_data(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=full"
    response = requests.get(url)
    data = response.json()

    if 'Time Series (Daily)' not in data:
        raise ValueError("Invalid API response")

    time_series = data['Time Series (Daily)']
    two_years_ago = datetime.now() - timedelta(days=730)

    for date_str, values in time_series.items():
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if date < two_years_ago.date():
            break

        StockData.objects.update_or_create(
            symbol=symbol,
            date=date,
            defaults={
                'open_price': values['1. open'],
                'high_price': values['2. high'],
                'low_price': values['3. low'],
                'close_price': values['4. close'],
                'volume': values['5. volume']
            }
        )