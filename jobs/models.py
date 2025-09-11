from django.db import models
from django.conf import settings

# Create your models here.


class Skill(models.Model):
    """Model to store job skills."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    """Model to store job postings."""

    # --- Choices for dropdown fields ---
    TECHNOLOGY_CHOICES = [
        ('PYTHON', 'Python'),
        ('JAVA', 'Java'),
        ('JAVASCRIPT', 'JavaScript'),
        ('NODEJS', 'Node.js'),
        ('REACT', 'React'),
    ]
    JOB_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('CONTRACT', 'Contract'),
        ('INTERNSHIP', 'Internship'),
    ]
    PURPOSE_CHOICES = [
        ('NEW_PROJECT', 'New Project'),
        ('REPLACEMENT', 'Replacement'),
        ('BACKFILL', 'Backfill'),
    ]
    PROJECT_TYPE_CHOICES = [
        ('INTERNAL', 'Internal'),
        ('EXTERNAL', 'External/Client'),
    ]
    EXPERIENCE_CHOICES = [
        ('0-1', '0-1 Years'),
        ('1-3', '1-3 Years'),
        ('3-5', '3-5 Years'),
        ('5-7', '5-7 Years'),
        ('7+', '7+ Years'),
    ]
    TENURE_CHOICES = [
        ('3_MONTHS', '3 Months'),
        ('6_MONTHS', '6 Months'),
        ('1_YEAR', '1 Year'),
        ('PERMANENT', 'Permanent'),
    ]
    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]
    TITLE_CHOICES = [
        ('SE', 'Software Engineer'),
        ('SSE', 'Senior Software Engineer'),
        ('LEAD', 'Tech Lead'),
        ('ARCH', 'Architect'),
    ]
    OPENINGS_CHOICES = [(i, str(i)) for i in range(1, 11)]

    # --- Model Fields ---
    title = models.CharField(max_length=50, choices=TITLE_CHOICES)
    project_name = models.CharField(max_length=255)
    technology = models.CharField(max_length=50, choices=TECHNOLOGY_CHOICES)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES)
    total_experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES)
    relevant_experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES)
    tenure = models.CharField(max_length=20, choices=TENURE_CHOICES)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    number_of_openings = models.IntegerField(choices=OPENINGS_CHOICES, null=True, blank=True)
    skills = models.ManyToManyField(Skill, help_text="Select at least 3 skills.")

    # --- ForeignKeys to User model ---
    floor_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='managed_jobs')
    project_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='pm_jobs')
    director_of_operation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='doo_jobs')
    first_round_interviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='first_round_interviews')
    second_round_interviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='second_round_interviews')

    def __str__(self):
        return f"{self.get_title_display()} - {self.project_name}"
