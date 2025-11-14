from django.db import models
from patients.models import Patient


class Equipment(models.Model):
    """Medical Equipment Tracking"""
    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        IN_USE = 'IN_USE', 'In Use'
        MAINTENANCE = 'MAINTENANCE', 'Under Maintenance'
        OUT_OF_SERVICE = 'OUT_OF_SERVICE', 'Out of Service'
    
    equipment_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    equipment_type = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE
    )
    
    location = models.CharField(max_length=100, help_text='Current location/room')
    
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    
    assigned_to_patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipment_assigned'
    )
    
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.equipment_id})"