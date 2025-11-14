# NEW - Complete updated file
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Health check view - React calls this to verify backend
def health_check(request):
    return JsonResponse({
        'status': 'success',
        'message': 'Django backend is running ✓',
        'api': 'http://127.0.0.1:8000/api/',
        'admin': 'http://127.0.0.1:8000/admin/',
    })

urlpatterns = [
    path('', health_check, name='home'),                    # ← NEW
    path('api/health/', health_check, name='api_health'),  # ← NEW
    path('admin/', admin.site.urls),
    path('', include('api_urls')),
]
