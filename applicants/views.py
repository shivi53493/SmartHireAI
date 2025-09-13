import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.files.storage import FileSystemStorage
from django.core.files import File

from .models import Applicant
from jobs.models import Job
from .forms import ApplicantForm
from . import resume_parser


@login_required
def applicant_list(request):
    """Displays a list of all applicants with pagination."""
    applicant_queryset = Applicant.objects.all().order_by('-created_at')
    jobs = Job.objects.all() # Get all jobs for the modal
    paginator = Paginator(applicant_queryset, 10)  # Show 10 applicants per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'applicants': page_obj,
        'jobs': jobs,
    }
    return render(request, 'applicants.html', context)


@login_required
def applicant_create(request):
    """Handles the creation of a new applicant from a full form."""
    job_id = request.GET.get('job')
    initial_data = {}

    # Check if data was passed from the resume parser via session
    if 'resume_data' in request.session:
        initial_data = request.session.pop('resume_data')  # Use and remove
        job_id = initial_data.get('job')

    job = get_object_or_404(Job, pk=job_id) if job_id else None
    initial_data['job'] = job

    if request.method == 'POST':
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            applicant = form.save(commit=False)
            # If a resume was parsed, its path is in the session. Attach it now.
            if 'resume_file_path' in request.session and not form.cleaned_data.get('resume'):
                file_path = request.session.pop('resume_file_path')
                with open(file_path, 'rb') as f:
                    applicant.resume.save(os.path.basename(file_path), File(f), save=False)

            applicant.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'New applicant has been added successfully!')
            # Clean up just in case it's still there
            if 'resume_file_path' in request.session:
                del request.session['resume_file_path']
            return redirect('applicants:applicant_list')
    else:
        form = ApplicantForm(initial=initial_data)

    return render(request, 'applicant_form.html', {'form': form, 'job': job})


@login_required
def applicant_detail(request, pk):
    """Displays the details of a single applicant."""
    applicant = get_object_or_404(Applicant, pk=pk)
    return render(request, 'applicant_detail.html', {'applicant': applicant})


@login_required
def applicant_update(request, pk):
    """Handles updating an existing applicant."""
    applicant = get_object_or_404(Applicant, pk=pk)
    if request.method == 'POST':
        form = ApplicantForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid():
            form.save()
            messages.success(request, f'Applicant "{applicant.full_name}" has been updated successfully!')
            return redirect('applicants:applicant_list')
    else:
        form = ApplicantForm(instance=applicant)

    context = {
        'form': form,
        'job': applicant.job,  # Pass the job for the header
    }
    return render(request, 'applicant_form.html', context)


@require_POST
@login_required
def parse_resume(request):
    """Parses an uploaded resume and returns extracted data or an error."""
    job_id = request.POST.get('job_id')
    resume_file = request.FILES.get('resume')

    if not job_id or not resume_file:
        return JsonResponse({'status': 'error', 'message': 'Job ID and resume file are required.'}, status=400)

    # Validate file type
    if not resume_file.name.lower().endswith(('.pdf', '.docx')):
        return JsonResponse({'status': 'error', 'message': 'Invalid file type. Please upload a PDF or DOCX file.'}, status=400)

    try:
        job = Job.objects.get(pk=job_id)
        job_skills = [skill.name for skill in job.skills.all()]

        # Extract text based on file type
        if resume_file.name.lower().endswith('.pdf'):
            text = resume_parser.extract_text_from_pdf(resume_file)
        else:  # .docx
            text = resume_parser.extract_text_from_docx(resume_file)

        resume_skills = resume_parser.extract_skills(text)
        match_score = resume_parser.calculate_match_score(resume_skills, job_skills)

        if match_score < 33:
            message = f"Resume rejected. Skill match is only {match_score:.0f}%. A minimum of 33% is required for the '{job.get_title_display()}' role."
            return JsonResponse({'status': 'error', 'message': message})

        # If successful, extract details and store in session
        extracted_details = resume_parser.extract_details(text)

        # Save the resume file temporarily
        fs = FileSystemStorage()
        filename = fs.save(resume_file.name, resume_file)

        request.session['resume_data'] = extracted_details
        request.session['resume_data']['job'] = job.pk
        request.session['resume_file_path'] = fs.path(filename)  # Store path to re-attach later

        return JsonResponse({'status': 'success', 'redirect_url': request.build_absolute_uri(f"/applicants/new/?job={job.pk}")})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
