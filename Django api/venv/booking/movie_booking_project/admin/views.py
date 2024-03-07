# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from bookings.models import Movie, Show
from .forms import MovieForm, ShowForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from bookings.models import Movie
from django.contrib.auth.decorators import user_passes_test

def  user_check(user):
    return user.username.endswith('@admin')


def list_movie(request):
    movies = Movie.objects.all()
    return render(request, 'list_movie.html', {'movies': movies})


@login_required(login_url='/adm/')
@user_passes_test(user_check,login_url='/adm/')
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movie added successfully')
            return redirect('movie_list')  # Adjust this to your actual URL name
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})


@login_required(login_url='/adm/')
@user_passes_test(user_check,login_url='/adm/')
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movie updated successfully')
            return redirect('movie_list')  # Adjust this to your actual URL name
    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit_movie.html', {'form': form, 'movie': movie})


@login_required(login_url='/adm/')
@user_passes_test(user_check,login_url='/adm/')
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Movie deleted successfully')
        return redirect('movie_list')  # Adjust this to your actual URL name
    return render(request, 'delete_movie.html', {'movie': movie})
# Repeat similar changes for add_show, edit_show, delete_show, disable_show views...


@login_required(login_url='/adm/')
@user_passes_test(user_check,login_url='/adm/')
def add_show(request):
    if request.method == 'POST':
        form = ShowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_show')  # Adjust this to your actual URL name
    else:
        form = ShowForm()
    return render(request, 'add_show.html', {'form': form})


@login_required(login_url='/adm/')
@user_passes_test(user_check,login_url='/adm/')
def edit_show(request, show_id):
    show = get_object_or_404(Show, pk=show_id)
    if request.method == 'POST':
        form = ShowForm(request.POST, instance=show)
        if form.is_valid():
            form.save()
            return redirect('list_show')  # Adjust this to your actual URL name
    else:
        form = ShowForm(instance=show)
    return render(request, 'edit_show.html', {'form': form, 'show': show})


@login_required(login_url='/adm/')
@user_passes_test(user_check,login_url='/adm/')
def delete_show(request, show_id):
    show = get_object_or_404(Show, pk=show_id)
    if request.method == 'POST':
        show.delete()
        return redirect('list_show')  # Adjust this to your actual URL name
    return render(request, 'delete_show.html', {'show': show})


@login_required(login_url='/adm/')
@user_passes_test(user_check,login_url='/adm/')
def disable_show(request, show_id):
    show = get_object_or_404(Show, pk=show_id)
    show.is_disabled = True
    show.save()
    return render(request, 'disable_show.html', {'message': 'Show disabled successfully'})


@login_required(login_url='/adm/')
@user_passes_test(user_check,login_url='/adm/')
def show_list(request):
    shows = Show.objects.all()
    return render(request, 'show_list.html', {'shows': shows})


# views.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log in the user immediately after signup
            messages.success(request, 'Signup successful. You are now logged in.')
            return redirect('movie_list')  # Adjust this to your actual URL name
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


# views.py
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('movie_list')  # Adjust this to your actual URL name
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# views.py
from django.contrib.auth import logout  # Import the logout function

# ... Your existing views ...

@login_required(login_url='/adm/')
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')  # Redirect to your login page, adjust the URL as needed


