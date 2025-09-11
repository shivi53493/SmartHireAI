from django.contrib import admin
from .models import Job, Skill

# Register your models here.

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_name', 'technology', 'priority', 'due_date', 'floor_manager')
    list_filter = ('technology', 'job_type', 'priority', 'due_date', 'floor_manager')
    search_fields = ('title', 'project_name', 'skills__name')
    filter_horizontal = ('skills',)
    raw_id_fields = ('floor_manager', 'project_manager', 'director_of_operation', 'first_round_interviewer', 'second_round_interviewer')

    fieldsets = (
        ('Job Details', {
            'fields': ('title', 'project_name', 'number_of_openings', 'skills')
        }),
        ('Requirements & Type', {
            'fields': ('technology', 'total_experience', 'relevant_experience', 'job_type', 'purpose', 'project_type', 'tenure')
        }),
        ('Management & Deadlines', {
            'fields': ('priority', 'due_date', 'floor_manager', 'project_manager', 'director_of_operation', 'first_round_interviewer', 'second_round_interviewer')
        }),
    )
