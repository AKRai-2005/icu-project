from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    CustomUser, DoctorProfile, DoctorDetail,
    NurseProfile, NurseDetail, Schedule
)
class DoctorDetailInline(admin.StackedInline):
    model = DoctorDetail
    can_delete = False
    verbose_name_plural = 'Doctor Details'
    fk_name = 'user'
    
    fieldsets = (
        ('Professional Information', {
            'fields': ('specialization', 'department')
        }),
        ('License & Certifications', {
            'fields': ('license_number', 'certifications')
        }),
    )

@admin.register(DoctorProfile)
class DoctorAdmin(UserAdmin):
    inlines = [DoctorDetailInline]
    
    list_display = [
        'username', 'get_full_name', 'email', 
        'get_specialization', 'employee_id', 
        'is_active', 'date_joined'
    ]
    list_filter = ['is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'employee_id']
    
    fieldsets = (
        ('Login Credentials', {
            'fields': ('username', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Contact Information', {
            'fields': ('contact_number', 'employee_id')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 
                      'first_name', 'last_name', 'employee_id', 
                      'contact_number', 'is_active')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role=CustomUser.UserRole.DOCTOR)
    
    def get_specialization(self, obj):
        try:
            return obj.doctor_detail.get_specialization_display()
        except DoctorDetail.DoesNotExist:
            return '-'
    get_specialization.short_description = 'Specialization'
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.role = CustomUser.UserRole.DOCTOR
            obj.is_staff = False
        super().save_model(request, obj, form, change)
class NurseDetailInline(admin.StackedInline):
    model = NurseDetail
    can_delete = False
    verbose_name_plural = 'Nurse Details'
    fk_name = 'user'
    
    fieldsets = (
        ('Work Information', {
            'fields': ('department', 'shift')
        }),
        ('License & Certifications', {
            'fields': ('license_number', 'certifications')
        }),
    )

@admin.register(NurseProfile)
class NurseAdmin(UserAdmin):
    inlines = [NurseDetailInline]
    
    list_display = [
        'username', 'get_full_name', 'email', 
        'get_shift', 'get_department', 'employee_id',
        'is_active', 'date_joined'
    ]
    list_filter = ['is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'employee_id']
    
    fieldsets = (
        ('Login Credentials', {
            'fields': ('username', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Contact Information', {
            'fields': ('contact_number', 'employee_id')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email',
                      'first_name', 'last_name', 'employee_id',
                      'contact_number', 'is_active')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role=CustomUser.UserRole.NURSE)
    
    def get_shift(self, obj):
        try:
            return obj.nurse_detail.get_shift_display()
        except NurseDetail.DoesNotExist:
            return '-'
    get_shift.short_description = 'Shift'
    
    def get_department(self, obj):
        try:
            return obj.nurse_detail.department
        except NurseDetail.DoesNotExist:
            return '-'
    get_department.short_description = 'Department'
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.role = CustomUser.UserRole.NURSE
            obj.is_staff = False
        super().save_model(request, obj, form, change)
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['staff', 'date', 'shift', 'department']
    list_filter = ['shift', 'date', 'department']
    search_fields = ['staff__username', 'staff__first_name', 'staff__last_name']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Staff & Timing', {
            'fields': ('staff', 'date', 'shift')
        }),
        ('Details', {
            'fields': ('department', 'notes')
        }),
    )