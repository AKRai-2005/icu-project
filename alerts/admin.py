from django.contrib import admin
from django.utils.html import format_html
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = [
        'alert_id', 'severity_badge', 'title',
        'patient', 'timestamp', 'acknowledged',
        'acknowledged_by'
    ]
    list_filter = ['severity', 'acknowledged', 'timestamp']
    search_fields = ['alert_id', 'title', 'message', 'patient__name']
    readonly_fields = ['alert_id', 'timestamp']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Alert Information', {
            'fields': ('alert_id', 'severity', 'title', 'message')
        }),
        ('Related Patient', {
            'fields': ('patient',)
        }),
        ('Acknowledgment', {
            'fields': (
                'acknowledged', 'acknowledged_by', 'acknowledged_at'
            )
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )
    
    def severity_badge(self, obj):
        colors = {
            'INFO': '#17a2b8',
            'WARNING': '#ffc107',
            'CRITICAL': '#dc3545'
        }
        color = colors.get(obj.severity, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_severity_display()
        )
    severity_badge.short_description = 'Severity'
    
    actions = ['mark_acknowledged']
    
    def mark_acknowledged(self, request, queryset):
        from django.utils import timezone
        queryset.update(
            acknowledged=True,
            acknowledged_by=request.user,
            acknowledged_at=timezone.now()
        )
    mark_acknowledged.short_description = "Mark selected alerts as acknowledged"