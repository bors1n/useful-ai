from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserRegisterForm
from tools.models import Favorite


def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}! Your account has been created successfully.')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Display user profile page with favorite tools."""
    # Get the user's favorite tools
    favorites = Favorite.objects.filter(user=request.user).select_related('tool')
    favorite_tools = [favorite.tool for favorite in favorites]
    
    context = {
        'favorite_tools': favorite_tools
    }
    
    return render(request, 'users/profile.html', context) 