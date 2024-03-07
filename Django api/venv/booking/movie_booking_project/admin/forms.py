# forms.py
from django import forms
from bookings.models import Movie, Show

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = '__all__'


# forms.py
from django import forms
from bookings.models import Show

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = '__all__'
