from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date
import uuid
# from django.contrib.auth.models import AbstractUser
#
#
# class CustomUser(AbstractUser):
#     phone_number = models.CharField(max_length=10)


class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=122)
    desc = models.TextField()

    def __str__(self):
        return self.name


class EventPage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=122)
    header = models.CharField(max_length=122)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.TextField(default='')
    price = models.IntegerField(default=10)
    tag = models.CharField(max_length=122, default='')
    eventdate = models.IntegerField(default=1)
    eventday = models.TextField(default="")
    eventmonth = models.TextField(default="")
    eventyear = models.IntegerField(default=2020)
    organizer = models.CharField(max_length=122, default='')

    def __str__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=25, null=True, blank=False)
    image_url = models.CharField(max_length=100000, null=True, blank=False)
    description = models.TextField(blank=False)
    genre = models.CharField(max_length=100)
    price = models.IntegerField(blank=False)

    def __str__(self):
        return self.title


class Theater(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField()

    def __str__(self):
        return f'{self.movie.title} at {self.theater.name}, {self.date} {self.time}'


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
 #   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seats = models.IntegerField()
    payment_status = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.showtime.movie.title} at {self.showtime.theater.name} ({self.showtime.date} {self.showtime.time}), {self.user.username}, {self.seats} seats'


class Eventbooking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_page = models.ForeignKey(EventPage, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    seats = models.IntegerField(default=1)
    date_booked = models.DateTimeField(auto_now_add=True)
    featured_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.event_page.title} Booking in the name of {self.name} for {self.event_page.title}'
