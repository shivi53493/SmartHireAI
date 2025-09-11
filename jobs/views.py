from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Job


# Create your views here.

@login_required
def job_list(request):
    """
    View to list all the jobs in a table.
    """
    # Fetch all jobs, ordering by the most recent due date
    # select_related('floor_manager') optimizes the query by fetching user details in the same database call
    jobs = Job.objects.select_related('floor_manager').all().order_by('-due_date')
    context = {'jobs': jobs}
    return render(request, 'jobs.html', context)
