# bookings/forms.py
from django import forms
from .models import Movie, Show, Booking


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title','image']  # Add other movie-related fields if needed

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['movie', 'show_time', 'date', 'is_disabled',]  # Add other show-related fields if needed

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'show',]  # Add other booking-related fields if needed


# # forms.py
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class AdminUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')



