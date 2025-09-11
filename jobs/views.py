from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job
from .forms import JobForm
from django.core.paginator import Paginator

@login_required
def job_list(request):
    """Displays a list of all jobs."""
    job_list_queryset = Job.objects.all().order_by('-due_date')
    paginator = Paginator(job_list_queryset, 10)  # Show 10 jobs per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs.html', {'jobs': page_obj})

@login_required
def job_create(request):
    """Handles the creation of a new job."""
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New job has been created successfully!')
            return redirect('job_list')
    else:
        form = JobForm()

    context = {
        'form': form,
    }
    return render(request, 'jobs_form.html', context)