from django.contrib import admin
from django.utils.html import format_html
from .models import Equipment

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = [
        'equipment_id', 'name', 'equipment_type',
        'status_badge', 'location',
        'assigned_to_patient', 'next_maintenance_date'
    ]
    list_filter = ['status', 'equipment_type', 'location']
    search_fields = ['equipment_id', 'name', 'location']
    
    fieldsets = (
        ('Equipment Information', {
            'fields': ('equipment_id', 'name', 'equipment_type', 'status')
        }),
        ('Location & Assignment', {
            'fields': ('location', 'assigned_to_patient')
        }),
        ('Maintenance Schedule', {
            'fields': ('last_maintenance_date', 'next_maintenance_date')
        }),
        ('Additional Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'AVAILABLE': '#28a745',
            'IN_USE': '#17a2b8',
            'MAINTENANCE': '#ffc107',
            'OUT_OF_SERVICE': '#dc3545'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'