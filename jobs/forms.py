from django import forms
from .models import Job, Skill
from django.contrib.auth import get_user_model

User = get_user_model()

class JobForm(forms.ModelForm):
    """Form for creating and updating Job instances."""

    class Meta:
        model = Job
        fields = [
            'title', 'project_name', 'technology', 'job_type', 'purpose',
            'project_type', 'total_experience', 'relevant_experience',
            'tenure', 'due_date', 'priority', 'number_of_openings', 'skills',
            'floor_manager', 'project_manager', 'director_of_operation',
            'first_round_interviewer', 'second_round_interviewer'
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'skills': forms.SelectMultiple(attrs={'size': '8'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Add Bootstrap classes to form fields and filter user querysets.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Use 'form-select' for dropdowns, 'form-control' for others
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_skills(self):
        """Validate that at least 3 skills are selected."""
        skills = self.cleaned_data.get('skills')
        if skills and len(skills) < 3:
            raise forms.ValidationError("Please select at least 3 skills.")
        return skills