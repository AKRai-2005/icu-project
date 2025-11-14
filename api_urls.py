from django.urls import path
# Import views from the staff app
from staff.views import (
    login_user,
    health_check,
    list_doctors,
    list_nurses
)
# Import views from the patients app
from patients.views import (
    list_create_patients,
    patient_detail_view
)

urlpatterns = [
    # Auth and Health Check routes (from staff.views)
    path('api/login/', login_user, name='login'),
    path('api/health/', health_check, name='health_check'),
    
    # Staff list routes (from staff.views)
    path('api/doctors/', list_doctors, name='list_doctors'),
    path('api/nurses/', list_nurses, name='list_nurses'),
    
    # Patient routes (from patients.views)
    path('api/patients/', list_create_patients, name='list_create_patients'),
    path('api/patients/<int:patient_id>/', patient_detail_view, name='patient_detail_view'),
]
