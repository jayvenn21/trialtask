# financial_backtester/urls.py
from django.urls import path
from data_fetcher.views import fetch_data
from backtester.views import run_backtest
from ml_predictor.views import predict_prices
from report_generator.views import generate_report

urlpatterns = [
    path('fetch-data/<str:symbol>/', fetch_data, name='fetch_data'),
    path('backtest/<str:symbol>/', run_backtest, name='run_backtest'),
    path('predict/<str:symbol>/', predict_prices, name='predict_prices'),
    path('report/<str:symbol>/', generate_report, name='generate_report'),
]

# Views in respective apps
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .utils import fetch_stock_data, backtest_strategy, predict_prices, generate_report, generate_json_report

@require_http_methods(["GET"])
def fetch_data(request, symbol):
    api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'
    fetch_stock_data(symbol, api_key)
    return JsonResponse({'status': 'success'})

@require_http_methods(["POST"])
def run_backtest(request, symbol):
    data = json.loads(request.body)
    results = backtest_strategy(symbol, data['initial_investment'], data['short_window'], data['long_window'])
    return JsonResponse(results)

@require_http_methods(["GET"])
def predict_prices(request, symbol):
    predictions = predict_prices(symbol)
    return JsonResponse({'predictions': predictions})

@require_http_methods(["GET"])
def generate_report(request, symbol):
    format = request.GET.get('format', 'pdf')
    backtest_results = backtest_strategy(symbol, 10000, 50, 200)
    predictions = predict_prices(symbol)
    actual_prices = list(StockData.objects.filter(symbol=symbol).order_by('-date')[:30].values_list('close_price', flat=True))

    if format == 'json':
        report = generate_json_report(backtest_results, predictions, actual_prices)
        return JsonResponse(json.loads(report))
    else:
        pdf_buffer = generate_report(backtest_results, predictions, actual_prices)
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{symbol}_report.pdf"'
        return response