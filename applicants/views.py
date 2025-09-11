from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Applicant
from jobs.models import Job
from .forms import ApplicantForm

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
    job = get_object_or_404(Job, pk=job_id) if job_id else None

    if request.method == 'POST':
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'New applicant has been added successfully!')
            return redirect('applicants:applicant_list')
    else:
        form = ApplicantForm(initial={'job': job})

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
        'job': applicant.job, # Pass the job for the header
    }
    return render(request, 'applicant_form.html', context)
