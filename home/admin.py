from django.contrib import admin
from home.models import Contact
from home.models import EventPage,Movie,Theater,Showtime,Booking,Eventbooking

# Register your models here.

admin.site.register(Contact)

admin.site.register(EventPage)

admin.site.register(Movie)

admin.site.register(Theater)

admin.site.register(Showtime)

admin.site.register(Booking)

admin.site.register(Eventbooking)