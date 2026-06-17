from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

from login import views
from login.services.cross_correlation_service import analyze_cross_correlation

def cross_correlation_page(request):
    """Render the Cross-Correlation Analysis page"""
    try:
        is_logged_in = (getattr(views, 'check', None) == "credit")
    except Exception:
        is_logged_in = False
        
    if not is_logged_in:
        return redirect('signin')

    # Retrieve sensor metadata from session
    sensors = request.session.get('cc_sensors', [])
    
    context = {
        'user_name': getattr(views, 'name', None) if is_logged_in else None,
        'sensors': sensors,
    }
    return render(request, 'cross-correlation.html', context)

def cross_correlation_analyze(request):
    """API endpoint to handle AJAX request for analysis"""
    try:
        is_logged_in = (getattr(views, 'check', None) == "credit")
    except Exception:
        is_logged_in = False
        
    if not is_logged_in:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor_a = data.get('sensor_a')
            sensor_b = data.get('sensor_b')
            
            if not sensor_a or not sensor_b:
                return JsonResponse({'error': 'Missing sensor selections'}, status=400)
                
            from_format = request.session.get('cc_from_format')
            to_format = request.session.get('cc_to_format')
            
            if not from_format or not to_format:
                return JsonResponse({'error': 'Missing timeframe data. Please generate a new visualization first.'}, status=400)
            
            # Call service to analyze
            result = analyze_cross_correlation(sensor_a, sensor_b, from_format, to_format)
            
            if 'error' in result:
                return JsonResponse({'error': result['error']}, status=400)
                
            return JsonResponse(result)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)
