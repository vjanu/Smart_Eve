from django import forms
from .models import Booking, Movie, Showtime


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['seats']
        widgets = {
            'seats': forms.NumberInput(attrs={'min': 1, 'max': 10, 'value': 1}),
        }


