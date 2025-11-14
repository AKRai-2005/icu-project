from django.db import models
from patients.models import Patient
from staff.models import CustomUser
import datetime


class Prescription(models.Model):
    """Medication Prescription"""
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        COMPLETED = 'COMPLETED', 'Completed'
        DISCONTINUED = 'DISCONTINUED', 'Discontinued'
    
    class Route(models.TextChoices):
        ORAL = 'ORAL', 'Oral'
        IV = 'IV', 'Intravenous'
        IM = 'IM', 'Intramuscular'
        SC = 'SC', 'Subcutaneous'
        TOPICAL = 'TOPICAL', 'Topical'
        INHALATION = 'INHALATION', 'Inhalation'
    
    prescription_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )
    
    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(
        max_length=100,
        help_text='e.g., Twice daily, Every 6 hours'
    )
    duration = models.CharField(
        max_length=100,
        help_text='e.g., 7 days, 2 weeks'
    )
    route = models.CharField(
        max_length=20,
        choices=Route.choices,
        default=Route.ORAL
    )
    
    instructions = models.TextField(
        help_text='Special instructions for administration'
    )
    notes = models.TextField(blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    prescribed_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    prescribed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': CustomUser.UserRole.DOCTOR}
    )
    
    class Meta:
        verbose_name = 'Prescription'
        verbose_name_plural = 'Prescriptions'
        ordering = ['-prescribed_date']
    
    def save(self, *args, **kwargs):
        if not self.prescription_id:
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            self.prescription_id = f"RX{timestamp}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.medicine_name} for {self.patient.name}"


class Treatment(models.Model):
    """Treatment Plan"""
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        URGENT = 'URGENT', 'Urgent'
    
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    treatment_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='treatments'
    )
    
    treatment_type = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    duration = models.CharField(max_length=100)
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    notes = models.TextField(blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    
    prescribed_date = models.DateTimeField(auto_now_add=True)
    prescribed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': CustomUser.UserRole.DOCTOR}
    )
    
    class Meta:
        verbose_name = 'Treatment Plan'
        verbose_name_plural = 'Treatment Plans'
        ordering = ['-prescribed_date']
    
    def save(self, *args, **kwargs):
        if not self.treatment_id:
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            self.treatment_id = f"TRT{timestamp}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.treatment_type} for {self.patient.name}"


class Admission(models.Model):
    """Patient Admission Record"""
    class AdmissionType(models.TextChoices):
        EMERGENCY = 'EMERGENCY', 'Emergency'
        ELECTIVE = 'ELECTIVE', 'Elective'
        TRANSFER = 'TRANSFER', 'Transfer'
    
    admission_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='admissions'
    )
    
    admission_type = models.CharField(
        max_length=20,
        choices=AdmissionType.choices
    )
    admission_datetime = models.DateTimeField()
    room_number = models.CharField(max_length=10)
    
    chief_complaint = models.TextField(
        help_text='Primary reason for admission'
    )
    
    initial_bp_systolic = models.IntegerField()
    initial_bp_diastolic = models.IntegerField()
    initial_heart_rate = models.IntegerField()
    initial_temperature = models.DecimalField(max_digits=4, decimal_places=1)
    initial_oxygen = models.IntegerField()
    
    emergency_contact_verified = models.BooleanField(default=False)
    insurance_verified = models.BooleanField(default=False)
    
    notes = models.TextField(blank=True)
    
    admitted_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role__in': [
            CustomUser.UserRole.NURSE,
            CustomUser.UserRole.ADMIN
        ]}
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Admission Record'
        verbose_name_plural = 'Admission Records'
        ordering = ['-admission_datetime']
    
    def save(self, *args, **kwargs):
        if not self.admission_id:
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            self.admission_id = f"ADM{timestamp}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Admission: {self.patient.name}"


class TreatmentHistory(models.Model):
    """Audit Trail for Patient Treatment"""
    class ActionType(models.TextChoices):
        REGISTRATION = 'REGISTRATION', 'Patient Registration'
        ADMISSION = 'ADMISSION', 'Admission'
        PRESCRIPTION = 'PRESCRIPTION', 'Prescription Added'
        TREATMENT = 'TREATMENT', 'Treatment Plan Added'
        VITALS = 'VITALS', 'Vitals Recorded'
        PROCEDURE = 'PROCEDURE', 'Procedure Performed'
        DISCHARGE = 'DISCHARGE', 'Discharge'
        OTHER = 'OTHER', 'Other'
    
    history_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='history'
    )
    
    action_type = models.CharField(max_length=20, choices=ActionType.choices)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    performed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True
    )
    
    related_prescription = models.ForeignKey(
        Prescription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    related_treatment = models.ForeignKey(
        Treatment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Treatment History'
        verbose_name_plural = 'Treatment Histories'
        ordering = ['-timestamp']
    
    def save(self, *args, **kwargs):
        if not self.history_id:
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            self.history_id = f"HIST{timestamp}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.patient.name} - {self.get_action_type_display()}"