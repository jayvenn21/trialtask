# report_generator/utils.py
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
import json

def generate_report(backtest_results, predictions, actual_prices):
    # Create plots
    plt.figure(figsize=(10, 5))
    plt.plot(actual_prices, label='Actual')
    plt.plot(predictions, label='Predicted')
    plt.legend()
    plt.title('Actual vs Predicted Stock Prices')
    plt.xlabel('Days')
    plt.ylabel('Price')
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # Generate PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Backtest Results")
    p.drawString(100, 730, f"Total Return: {backtest_results['total_return']:.2%}")
    p.drawString(100, 710, f"Max Drawdown: {backtest_results['max_drawdown']:.2%}")
    p.drawString(100, 690, f"Number of Trades: {backtest_results['num_trades']}")
    p.drawImage(img_buffer, 100, 400, width=400, height=200)
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

def generate_json_report(backtest_results, predictions, actual_prices):
    return json.dumps({
        'backtest_results': backtest_results,
        'predictions': predictions,
        'actual_prices': actual_prices
    })