from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import UserProfile

def register_view(request):
    """
    Handles user registration with validation and automatic login.
    """
    if request.user.is_authenticated:
        return redirect('products:product_list')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        errors = []
        if not username or len(username) < 3:
            errors.append("Username must be at least 3 characters long.")
        if User.objects.filter(username__iexact=username).exists():
            errors.append("Username is already taken.")
        if not email:
            errors.append("Email address is required.")
        elif User.objects.filter(email__iexact=email).exists():
            errors.append("An account with that email already exists.")
        if not password or len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if password != password_confirm:
            errors.append("Passwords do not match.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'users/register.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)
        messages.success(request, f"Welcome to Auspify Shop, {user.first_name or user.username}! Your account has been created.")
        return redirect('products:product_list')

    return render(request, 'users/register.html')


def login_view(request):
    """
    Handles user authentication and session creation.
    """
    if request.user.is_authenticated:
        return redirect('products:product_list')

    next_url = request.GET.get('next', request.POST.get('next', 'products:product_list'))

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect('products:product_list')
            else:
                messages.error(request, "Your account has been deactivated.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'users/login.html', {'next': next_url})


def logout_view(request):
    """
    Terminates user session and redirects to storefront.
    """
    logout(request)
    messages.info(request, "You have been signed out successfully.")
    return redirect('products:home')


@login_required(login_url='users:login')
def profile_view(request):
    """
    View and update user personal profile and shipping address.
    """
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        # Update User model fields
        request.user.first_name = first_name
        request.user.last_name = last_name
        if email and email != request.user.email:
            if User.objects.filter(email__iexact=email).exclude(pk=request.user.pk).exists():
                messages.error(request, "That email is already registered to another account.")
                return render(request, 'users/profile.html', {'profile': profile})
            request.user.email = email
        request.user.save()

        # Update Profile fields
        profile.phone_number = request.POST.get('phone_number', '').strip()
        profile.address_line_1 = request.POST.get('address_line_1', '').strip()
        profile.address_line_2 = request.POST.get('address_line_2', '').strip()
        profile.city = request.POST.get('city', '').strip()
        profile.state = request.POST.get('state', '').strip()
        profile.postal_code = request.POST.get('postal_code', '').strip()
        profile.country = request.POST.get('country', 'India').strip()
        profile.save()

        messages.success(request, "Your profile information has been saved successfully.")
        return redirect('users:profile')

    return render(request, 'users/profile.html', {'profile': profile})
