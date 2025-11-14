from django.contrib import admin
from django.utils.html import format_html
from .models import Patient, Vitals

class VitalsInline(admin.TabularInline):
    model = Vitals
    extra = 1
    fields = [
        'heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
        'temperature', 'oxygen_saturation', 'respiratory_rate',
        'recorded_by', 'notes'
    ]
    readonly_fields = ['recorded_at']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    inlines = [VitalsInline]
    
    list_display = [
        'patient_id', 'name', 'age', 'gender',
        'room_number', 'status_badge', 'attending_physician',
        'admission_date'
    ]
    
    list_filter = ['status', 'gender', 'admission_date', 'insurance_verified']
    search_fields = ['patient_id', 'name', 'contact_number', 'diagnosis']
    readonly_fields = ['patient_id', 'admission_date', 'created_at', 'updated_at']
    date_hierarchy = 'admission_date'
    
    fieldsets = (
        ('Patient Identification', {
            'fields': ('patient_id', 'name', 'age', 'gender', 'date_of_birth')
        }),
        ('Contact Information', {
            'fields': (
                'contact_number', 
                'emergency_contact_name',
                'emergency_contact'
            )
        }),
        ('Medical Information', {
            'fields': ('diagnosis', 'medical_history', 'status')
        }),
        ('ICU Assignment', {
            'fields': (
                'room_number', 'bed_number',
                'attending_physician', 'admitted_by'
            )
        }),
        ('Insurance & Verification', {
            'fields': ('insurance_id', 'insurance_verified'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('additional_notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('admission_date', 'discharge_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'CRITICAL': '#dc3545',
            'STABLE': '#28a745',
            'RECOVERING': '#17a2b8',
            'DISCHARGED': '#6c757d',
            'TRANSFERRED': '#ffc107'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

@admin.register(Vitals)
class VitalsAdmin(admin.ModelAdmin):
    list_display = [
        'patient', 'heart_rate', 'blood_pressure', 
        'temperature', 'oxygen_saturation',
        'recorded_at', 'recorded_by'
    ]
    list_filter = ['recorded_at', 'recorded_by']
    search_fields = ['patient__name', 'patient__patient_id']
    readonly_fields = ['recorded_at']
    date_hierarchy = 'recorded_at'
    
    fieldsets = (
        ('Patient', {
            'fields': ('patient',)
        }),
        ('Vital Signs', {
            'fields': (
                'heart_rate',
                ('blood_pressure_systolic', 'blood_pressure_diastolic'),
                'temperature',
                'oxygen_saturation',
                'respiratory_rate'
            )
        }),
        ('Recording Information', {
            'fields': ('recorded_by', 'recorded_at', 'notes')
        }),
    )