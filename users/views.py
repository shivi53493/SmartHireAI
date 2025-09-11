from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard',{'user': request.user})
  

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([full_name, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('signup')

        user = User.objects.create_user(email=email, password=password, full_name=full_name)
        auth_login(request, user)
        messages.success(request, "Registration successful. Welcome to SmartHireAI!")
        return redirect('dashboard')
      

    return render(request, 'signup.html')




def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')



def logout(request):
    auth_logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('home')

@login_required
def dashboard(request):

    return render(request, 'dashboard.html')