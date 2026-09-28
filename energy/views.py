import csv
import numpy as np
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from sklearn.metrics import r2_score

from src.data_loader import load_data
from src.model import train_model
from src.bill import calculate_tneb_bill

# Cache for trained models (loaded once at startup)
_cached_models = None
_cached_scores = None
_cached_test_data = None


def get_cached_models():
    """Load or retrieve cached trained models"""
    global _cached_models, _cached_scores, _cached_test_data
    
    if _cached_models is None:
        print("-> Training models (this happens only once)...")
        data = load_data()
        lr, dt, rf, X_test, y_test = train_model(data)
        
        lr_score = round(r2_score(y_test, lr.predict(X_test)), 2)
        dt_score = round(r2_score(y_test, dt.predict(X_test)), 2)
        rf_score = round(r2_score(y_test, rf.predict(X_test)), 2)
        
        _cached_models = (lr, dt, rf)
        _cached_scores = (lr_score, dt_score, rf_score)
        _cached_test_data = (X_test, y_test)
        print("[OK] Models cached successfully!")
    
    return _cached_models, _cached_scores, _cached_test_data


def compute_prediction_data(voltage, intensity):
    # Use cached models instead of retraining
    (lr, dt, rf), (lr_score, dt_score, rf_score), (X_test, y_test) = get_cached_models()

    def format_hour(hour):
        if hour == 0:
            return '12 AM'
        if hour < 12:
            return f'{hour} AM'
        if hour == 12:
            return '12 PM'
        return f'{hour - 12} PM'

    daily_energy = 0.0
    hourly_data = []

    for hour in range(24):
        random_noise = np.random.normal(0, 1)
        user_data = np.array([[hour, voltage, intensity, random_noise]])
        pred = rf.predict(user_data)[0]

        if 6 <= hour <= 9:
            pred *= 1.1
        elif 18 <= hour <= 22:
            pred *= 1.2
        elif 0 <= hour <= 5:
            pred *= 0.8

        hourly_data.append((hour, format_hour(hour), pred))
        daily_energy += pred

    daily_energy *= 0.2
    units = daily_energy * 30

    peak_index = int(np.argmax([value for _, _, value in hourly_data]))
    peak_period = f"{format_hour(peak_index)} – {format_hour((peak_index + 3) % 24)}"

    if intensity >= 18 or daily_energy > 50:
        precaution = 'High energy use detected. Reduce heavy appliance use and avoid peak-hour consumption.'
    elif daily_energy > 35:
        precaution = 'Moderate energy consumption. Shift usage to off-peak hours where possible.'
    else:
        precaution = 'Energy usage looks balanced. Continue monitoring and prefer efficient devices.'

    max_val = max(value for _, _, value in hourly_data) if hourly_data else 1
    formatted_hourly_data = []

    for hour, label, value in hourly_data:
        height = round((value / max_val) * 140 + 20, 1)
        formatted_hourly_data.append({
            'hour': hour,
            'label': label,
            'value': round(value, 2),
            'height': height,
        })

    return {
        'lr_score': lr_score,
        'dt_score': dt_score,
        'rf_score': rf_score,
        'prediction': round(daily_energy, 2),
        'units': round(units, 2),
        'bill': round(calculate_tneb_bill(units), 2),
        'peak_period': peak_period,
        'precaution': precaution,
        'hourly_data': formatted_hourly_data,
    }


from django.template.loader import render_to_string

@require_GET
def home(request):
    voltage = float(request.GET.get('voltage', 220.0))
    intensity = float(request.GET.get('intensity', 10.0))
    context = {
        'voltage': voltage,
        'intensity': intensity,
        'prediction': None,
        'units': None,
        'bill': None,
        'lr_score': None,
        'dt_score': None,
        'rf_score': None,
        'error': None,
        'powerbi_csv_url': None,
        'powerbi_json_url': None,
    }

    try:
        prediction_data = compute_prediction_data(voltage, intensity)
        context.update(prediction_data)

        scheme = 'https' if request.is_secure() else 'http'
        base_url = f"{scheme}://{request.get_host()}"
        context['powerbi_csv_url'] = f"{base_url}/data.csv?voltage={voltage}&intensity={intensity}"
        context['powerbi_json_url'] = f"{base_url}/data.json?voltage={voltage}&intensity={intensity}"
    except Exception as exc:
        context['error'] = str(exc)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return only the results part for AJAX
        results_html = render_to_string('energy/results.html', context)
        return HttpResponse(results_html)

    return render(request, 'energy/index.html', context)



@require_GET
def export_predictions_csv(request):
    voltage = float(request.GET.get('voltage', 220.0))
    intensity = float(request.GET.get('intensity', 10.0))
    prediction_data = compute_prediction_data(voltage, intensity)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="energy_predictions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Hour', 'Label', 'Predicted_kWh'])
    for item in prediction_data['hourly_data']:
        writer.writerow([item['hour'], item['label'], item['value']])

    writer.writerow([])
    writer.writerow(['Daily energy', prediction_data['prediction']])
    writer.writerow(['Monthly units', prediction_data['units']])
    writer.writerow(['Estimated bill', prediction_data['bill']])
    writer.writerow(['Peak consumption', prediction_data['peak_period']])
    writer.writerow(['Linear Regression score', prediction_data['lr_score']])
    writer.writerow(['Decision Tree score', prediction_data['dt_score']])
    writer.writerow(['Random Forest score', prediction_data['rf_score']])
    writer.writerow(['Precaution', prediction_data['precaution']])

    return response


@require_GET
def export_predictions_json(request):
    voltage = float(request.GET.get('voltage', 220.0))
    intensity = float(request.GET.get('intensity', 10.0))
    prediction_data = compute_prediction_data(voltage, intensity)
    return JsonResponse(prediction_data)
