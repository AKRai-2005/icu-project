from django.db import models
from staff.models import CustomUser
import datetime


class Patient(models.Model):
    """Patient Information Model"""
    class Status(models.TextChoices):
        CRITICAL = 'CRITICAL', 'Critical'
        STABLE = 'STABLE', 'Stable'
        RECOVERING = 'RECOVERING', 'Recovering'
        DISCHARGED = 'DISCHARGED', 'Discharged'
        TRANSFERRED = 'TRANSFERRED', 'Transferred'
    
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'
    
    # Basic Information
    patient_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=Gender.choices)
    date_of_birth = models.DateField()
    
    # Contact Information
    contact_number = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    emergency_contact_name = models.CharField(max_length=200)
    
    # Medical Information
    diagnosis = models.TextField()
    medical_history = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.STABLE
    )
    
    # ICU Details
    room_number = models.CharField(max_length=10)
    bed_number = models.CharField(max_length=10, blank=True)
    admission_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(null=True, blank=True)
    
    # Insurance & Admin
    insurance_id = models.CharField(max_length=100, blank=True)
    insurance_verified = models.BooleanField(default=False)
    
    # Assignment
    attending_physician = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': CustomUser.UserRole.DOCTOR},
        related_name='patients'
    )
    
    admitted_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='admitted_patients'
    )
    
    additional_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['-admission_date']
    
    def save(self, *args, **kwargs):
        if not self.patient_id:
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            self.patient_id = f"PAT{timestamp}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - Room {self.room_number} ({self.get_status_display()})"


class Vitals(models.Model):
    """Vital Signs Monitoring"""
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='vitals'
    )
    heart_rate = models.IntegerField(help_text='Beats per minute')
    blood_pressure_systolic = models.IntegerField()
    blood_pressure_diastolic = models.IntegerField()
    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        help_text='Temperature in Celsius'
    )
    oxygen_saturation = models.IntegerField(help_text='Percentage')
    respiratory_rate = models.IntegerField(blank=True, null=True)
    
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True
    )
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Vital Signs'
        verbose_name_plural = 'Vital Signs'
        ordering = ['-recorded_at']
    
    @property
    def blood_pressure(self):
        return f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}"
    
    def __str__(self):
        return f"{self.patient.name} - {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"