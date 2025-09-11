from django.db import models
from jobs.models import Skill, Job # Reusing models from the jobs app

# Create your models here.
class Applicant(models.Model):
    """Model to store applicant details."""

    # --- Choices for dropdown fields ---
    TITLE_CHOICES = [
        ('MR', 'Mr.'),
        ('MRS', 'Mrs.'),
        ('MS', 'Ms.'),
        ('DR', 'Dr.'),
    ]
    QUALIFICATION_CHOICES = [
        ('HIGH_SCHOOL', 'High School'),
        ('DIPLOMA', 'Diploma'),
        ('BACHELORS', 'Bachelor\'s Degree'),
        ('MASTERS', 'Master\'s Degree'),
        ('PHD', 'PhD'),
    ]
    TECHNOLOGY_CHOICES = [
        ('PYTHON', 'Python'),
        ('JAVA', 'Java'),
        ('JAVASCRIPT', 'JavaScript'),
        ('NODEJS', 'Node.js'),
        ('REACT', 'React'),
        ('DOT_NET', '.NET'),
        ('DEVOPS', 'DevOps'),
    ]
    STATE_CHOICES = [
        ('DL', 'Delhi'),
        ('MH', 'Maharashtra'),
        ('KA', 'Karnataka'),
        ('TN', 'Tamil Nadu'),
        ('UP', 'Uttar Pradesh'),
    ]
    CITY_CHOICES = [
        ('DEL', 'Delhi'),
        ('MUM', 'Mumbai'),
        ('BLR', 'Bangalore'),
        ('CHN', 'Chennai'),
        ('LKO', 'Lucknow'),
    ]

    # --- Personal / Employment Details ---
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    title = models.CharField(max_length=10, choices=TITLE_CHOICES)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    total_experience_months = models.PositiveIntegerField(help_text="Total experience in months.")
    current_company = models.CharField(max_length=255, blank=True, null=True)
    current_position = models.CharField(max_length=255)
    notice_period_days = models.PositiveIntegerField(help_text="Notice period in days.")
    highest_qualification = models.CharField(max_length=50, choices=QUALIFICATION_CHOICES)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True, help_text="Attach resume file.")

    # --- Contact Details ---
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    is_whatsapp_number = models.BooleanField(default=False, verbose_name="Registered with WhatsApp")
    whatsapp_number = models.CharField(max_length=15)

    # --- Skill Details ---
    technology = models.CharField(max_length=50, choices=TECHNOLOGY_CHOICES)
    primary_skills = models.ManyToManyField(Skill, blank=True, related_name="skilled_applicants")

    # --- Demographic Details ---
    house_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="House No/Flat No")
    street_address = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=50, choices=STATE_CHOICES)
    city = models.CharField(max_length=50, choices=CITY_CHOICES)
    pin_code = models.CharField(max_length=10, blank=True, null=True)

    # --- Timestamps for tracking ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.get_title_display()} {self.first_name} {self.last_name}"
