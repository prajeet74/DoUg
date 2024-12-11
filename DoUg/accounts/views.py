from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomLoginForm, UserProfileSetupForm
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import CustomUser

@unauthenticated_user
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Assign user to the "customerss" group
            customers_group = Group.objects.get(name='customers')
            user.groups.add(customers_group)
            
            # Pass the backend explicitly when logging the user in
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Or specify your custom backend if needed
            return redirect('profile_setup')  # Redirect to profile setup page
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/registers.html', {'form': form})

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            # Get the email and password from the form
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Authenticate the user using email and password
            try:
                user = CustomUser.objects.get(email=email)  # Fetch user based on email
                if user.check_password(password):  # Verify password
                    # Specify the backend explicitly for login
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)

                    # Handle "Remember Me"
                    if form.cleaned_data.get('remember_me'):
                        request.session.set_expiry(1209600)  # Set expiry to 2 weeks (1209600 seconds)

                    return redirect('home')  # Redirect to the home page
                else:
                    messages.error(request, "Invalid email or password.")  # Incorrect password
            except CustomUser.DoesNotExist:
                messages.error(request, "Invalid email or password.")  # User not found
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/logins.html', {'form': form})


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customers'])


@login_required(login_url='login')
@admin_only
def admin_view(request):
    return render(request, 'accounts/admin.html')

@login_required
def profile_setup(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileSetupForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to homepage or dashboard after profile setup
    else:
        form = UserProfileSetupForm(instance=user)
    
    return render(request, 'accounts/profile_setup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout