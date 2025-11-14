from django.contrib import admin
from django.utils.html import format_html
from .models import Prescription, Treatment, Admission, TreatmentHistory

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = [
        'prescription_id', 'patient', 'medicine_name',
        'dosage', 'frequency', 'status',
        'prescribed_by', 'prescribed_date'
    ]
    list_filter = ['status', 'route', 'prescribed_date']
    search_fields = [
        'prescription_id', 'patient__name', 
        'medicine_name', 'patient__patient_id'
    ]
    readonly_fields = ['prescription_id', 'prescribed_date']
    date_hierarchy = 'prescribed_date'
    
    fieldsets = (
        ('Prescription Information', {
            'fields': ('prescription_id', 'patient', 'status')
        }),
        ('Medication Details', {
            'fields': (
                'medicine_name', 'dosage', 'frequency',
                'duration', 'route'
            )
        }),
        ('Instructions', {
            'fields': ('instructions', 'notes')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'prescribed_date')
        }),
        ('Prescribed By', {
            'fields': ('prescribed_by',)
        }),
    )

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = [
        'treatment_id', 'patient', 'treatment_type',
        'priority_badge', 'status', 'follow_up_required',
        'prescribed_by', 'prescribed_date'
    ]
    list_filter = ['priority', 'status', 'follow_up_required', 'prescribed_date']
    search_fields = [
        'treatment_id', 'patient__name', 
        'treatment_type', 'patient__patient_id'
    ]
    readonly_fields = ['treatment_id', 'prescribed_date']
    date_hierarchy = 'prescribed_date'
    
    fieldsets = (
        ('Treatment Information', {
            'fields': ('treatment_id', 'patient', 'status')
        }),
        ('Treatment Details', {
            'fields': (
                'treatment_type', 'description',
                'priority', 'duration'
            )
        }),
        ('Follow-up', {
            'fields': ('follow_up_required', 'follow_up_date')
        }),
        ('Additional Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Prescribed Information', {
            'fields': ('prescribed_by', 'prescribed_date')
        }),
    )
    
    def priority_badge(self, obj):
        colors = {
            'LOW': '#28a745',
            'MEDIUM': '#ffc107',
            'HIGH': '#fd7e14',
            'URGENT': '#dc3545'
        }
        color = colors.get(obj.priority, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = [
        'admission_id', 'patient', 'admission_type',
        'room_number', 'admission_datetime',
        'emergency_contact_verified', 'insurance_verified',
        'admitted_by'
    ]
    list_filter = [
        'admission_type', 'emergency_contact_verified',
        'insurance_verified', 'admission_datetime'
    ]
    search_fields = [
        'admission_id', 'patient__name', 
        'patient__patient_id', 'room_number'
    ]
    readonly_fields = ['admission_id', 'created_at']
    date_hierarchy = 'admission_datetime'
    
    fieldsets = (
        ('Admission Information', {
            'fields': (
                'admission_id', 'patient', 'admission_type',
                'admission_datetime', 'room_number'
            )
        }),
        ('Chief Complaint', {
            'fields': ('chief_complaint',)
        }),
        ('Initial Vitals', {
            'fields': (
                ('initial_bp_systolic', 'initial_bp_diastolic'),
                'initial_heart_rate',
                'initial_temperature',
                'initial_oxygen'
            )
        }),
        ('Verification', {
            'fields': (
                'emergency_contact_verified',
                'insurance_verified'
            )
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Admitted By', {
            'fields': ('admitted_by', 'created_at')
        }),
    )

@admin.register(TreatmentHistory)
class TreatmentHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'history_id', 'patient', 'action_type',
        'description_short', 'performed_by', 'timestamp'
    ]
    list_filter = ['action_type', 'timestamp']
    search_fields = [
        'history_id', 'patient__name',
        'patient__patient_id', 'description'
    ]
    readonly_fields = ['history_id', 'timestamp']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('History Record', {
            'fields': ('history_id', 'patient', 'action_type')
        }),
        ('Details', {
            'fields': ('description', 'performed_by', 'timestamp')
        }),
        ('Related Records', {
            'fields': ('related_prescription', 'related_treatment'),
            'classes': ('collapse',)
        }),
    )
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'