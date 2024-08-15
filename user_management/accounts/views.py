from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from .models import CustomUser
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages



def home(request):
    return render(request, 'signup.html')



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        
        email = request.POST.get('email')
        username = request.POST.get('username')

        # Check if the user already exists
        if CustomUser.objects.filter(email=email).exists() or CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'User already exists! try a different username.')
            return redirect('signup')

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Signup successful!')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
  
        
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data.get('user_type')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user_type and user.user_type != user_type:
                    messages.error(request, 'User type does not match.')
                    return redirect('login')
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                
                # Check user type and redirect accordingly
                if hasattr(user, 'user_type'):
                    if user.user_type == 'Doctor':
                        return redirect('doctor_dashboard')
                    elif user.user_type == 'Patient':
                        return redirect('patient_dashboard')
                else:
                    # Fallback if user_type is not set
                    return redirect('dashboard')

            else:
                messages.error(request, 'Invalid email or password.')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html', {'user': request.user})


def doctor_dashboard(request):
    if request.user.user_type != 'Doctor':
        return redirect('login')
    
    return render(request, 'doctor_dashboard.html',{'user': request.user})

def patient_dashboard(request):
    if request.user.user_type != 'Patient':
        return redirect('login')
    
    return render(request, 'patient_dashboard.html',{'user': request.user})