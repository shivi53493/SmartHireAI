from django.contrib import admin
from .models import Applicant

# Register your models here.
@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'technology', 'total_experience_months', 'created_at')
    list_filter = ('technology', 'state', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'primary_skills__name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Personal Information', {
            'fields': ('title', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'resume')
        }),
        ('Employment Details', {
            'fields': ('total_experience_months', 'current_company', 'current_position', 'notice_period_days', 'highest_qualification')
        }),
        ('Contact Details', {
            'fields': ('email', 'mobile_number', 'is_whatsapp_number', 'whatsapp_number')
        }),
        ('Skill Details', {
            'fields': ('technology', 'primary_skills')
        }),
        ('Demographic Details', {
            'fields': ('house_number', 'street_address', 'state', 'city', 'pin_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) # Hides this section by default
        }),
    )
