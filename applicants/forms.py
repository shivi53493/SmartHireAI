from django import forms
from .models import Applicant

class ApplicantForm(forms.ModelForm):
    """Form for creating a new Applicant."""

    class Meta:
        model = Applicant
        fields = [
            'job', 'title', 'first_name', 'middle_name', 'last_name', 'date_of_birth',
            'total_experience_months', 'current_company', 'current_position',
            'notice_period_days', 'highest_qualification', 'resume', 'email',
            'mobile_number', 'is_whatsapp_number', 'whatsapp_number', 'technology',
            'primary_skills', 'house_number', 'street_address', 'state', 'city', 'pin_code'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'primary_skills': forms.SelectMultiple(attrs={'size': '8'}),
            'job': forms.HiddenInput(), # The job is pre-selected, so we hide it.
        }

    def __init__(self, *args, **kwargs):
        """
        Add Bootstrap classes to form fields.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Skip the hidden job field
            if field_name == 'job':
                continue
            # Use 'form-select' for dropdowns, 'form-control' for others
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
