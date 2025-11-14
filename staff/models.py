from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    """Custom manager for CustomUser"""
    pass


class CustomUser(AbstractUser):
    """Custom User Model with Role Support"""
    class UserRole(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        DOCTOR = 'DOCTOR', 'Doctor'
        NURSE = 'NURSE', 'Nurse'
    
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.ADMIN
    )
    employee_id = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )
    contact_number = models.CharField(
        max_length=15,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# DOCTOR PROXY MODEL
class DoctorProfile(CustomUser):
    """Proxy model for Doctors"""
    
    class Meta:
        proxy = True
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = CustomUser.UserRole.DOCTOR
        return super().save(*args, **kwargs)


# DOCTOR DETAIL MODEL
class DoctorDetail(models.Model):
    """Extended Doctor Information"""
    class Specialization(models.TextChoices):
        PULMONOLOGY = 'PULMONOLOGY', 'Pulmonology'
        CRITICAL_CARE = 'CRITICAL_CARE', 'Critical Care'
        CARDIOLOGY = 'CARDIOLOGY', 'Cardiology'
        EMERGENCY = 'EMERGENCY', 'Emergency Medicine'
        NEUROLOGY = 'NEUROLOGY', 'Neurology'
        SURGERY = 'SURGERY', 'Surgery'
        ANESTHESIOLOGY = 'ANESTHESIOLOGY', 'Anesthesiology'
        GENERAL = 'GENERAL', 'General Medicine'
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': CustomUser.UserRole.DOCTOR},
        related_name='doctor_detail'
    )
    specialization = models.CharField(
        max_length=50,
        choices=Specialization.choices
    )
    department = models.CharField(max_length=100)
    license_number = models.CharField(
        max_length=100,
        unique=True
    )
    certifications = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Doctor Detail'
        verbose_name_plural = 'Doctor Details'
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.get_specialization_display()}"


# NURSE PROXY MODEL
class NurseProfile(CustomUser):
    """Proxy model for Nurses"""
    
    class Meta:
        proxy = True
        verbose_name = 'Nurse'
        verbose_name_plural = 'Nurses'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = CustomUser.UserRole.NURSE
        return super().save(*args, **kwargs)


# NURSE DETAIL MODEL
class NurseDetail(models.Model):
    """Extended Nurse Information"""
    class Shift(models.TextChoices):
        MORNING = 'MORNING', 'Morning (6AM - 2PM)'
        AFTERNOON = 'AFTERNOON', 'Afternoon (2PM - 10PM)'
        NIGHT = 'NIGHT', 'Night (10PM - 6AM)'
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': CustomUser.UserRole.NURSE},
        related_name='nurse_detail'
    )
    department = models.CharField(max_length=100)
    shift = models.CharField(
        max_length=20,
        choices=Shift.choices
    )
    license_number = models.CharField(
        max_length=100,
        unique=True
    )
    certifications = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Nurse Detail'
        verbose_name_plural = 'Nurse Details'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_shift_display()}"


# SCHEDULE MODEL
class Schedule(models.Model):
    """Staff Schedule Management"""
    staff = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role__in': [
            CustomUser.UserRole.DOCTOR,
            CustomUser.UserRole.NURSE
        ]}
    )
    shift = models.CharField(
        max_length=20,
        choices=NurseDetail.Shift.choices
    )
    date = models.DateField()
    department = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Staff Schedule'
        verbose_name_plural = 'Staff Schedules'
        ordering = ['-date', 'shift']
        unique_together = ['staff', 'date', 'shift']
    
    def __str__(self):
        return f"{self.staff.get_full_name()} - {self.date} ({self.shift})"