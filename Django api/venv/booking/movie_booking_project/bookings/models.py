# bookings/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import time
import uuid

# movies/models.py
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='movie_images/', null=True, blank=False)

    def __str__(self):
        return self.title


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    TIME_CHOICES = [
        (time(11, 30), '11:30 AM'),
        (time(14, 30), '2:30 PM'),
        (time(17, 0), '5:00 PM'),
        (time(21, 0), '9:00 PM'),
    ]

    show_time = models.TimeField(choices=TIME_CHOICES)
    date = models.DateField()
    is_disabled = models.BooleanField(default=False)
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, default=150.00) 

    def __str__(self):
        return f"{self.movie.title} - {self.get_show_time_display()}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=8, default=uuid.uuid4().hex[:8]) 
    no_of_tickets = models.PositiveIntegerField(default=1)  # Add this field
    is_confirmed = models.BooleanField(default=False)  # Add this field
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    # Add other booking-related fields

    def __str__(self):
        return f"Booking #{self.id} - {self.show}"
