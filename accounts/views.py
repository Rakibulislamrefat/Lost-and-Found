from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm


def register_view(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    """User logout."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    """User profile page."""
    user_items = request.user.items.all()
    user_claims = request.user.claims.all()
    context = {
        'user_items': user_items,
        'user_claims': user_claims,
    }
    return render(request, 'accounts/profile.html', context)
