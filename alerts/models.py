from django.db import models
from patients.models import Patient
from staff.models import CustomUser
import datetime


class Alert(models.Model):
    """System Alerts and Notifications"""
    class Severity(models.TextChoices):
        INFO = 'INFO', 'Info'
        WARNING = 'WARNING', 'Warning'
        CRITICAL = 'CRITICAL', 'Critical'
    
    alert_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )
    
    severity = models.CharField(max_length=20, choices=Severity.choices)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='alerts'
    )
    
    timestamp = models.DateTimeField(auto_now_add=True)
    acknowledged = models.BooleanField(default=False)
    acknowledged_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'
        ordering = ['-timestamp']
    
    def save(self, *args, **kwargs):
        if not self.alert_id:
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            self.alert_id = f"ALT{timestamp}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        patient_info = f" - {self.patient.name}" if self.patient else ""
        return f"{self.get_severity_display()}: {self.title}{patient_info}"