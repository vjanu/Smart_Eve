from django import forms
from .models import Booking, Movie, Showtime, Eventbooking, EventPage


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seats']
        labels = {
            'seats': "Select your Seat Below "
        }
        widgets = {
            'seats': forms.NumberInput(attrs={'min': 1, 'max': 10, 'value': 1,'id': 'seats-field'}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Eventbooking
        fields = ['event_page', 'name', 'featured_price']

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=10)
    seats = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        event_id = kwargs.pop('event_id')
        super().__init__(*args, **kwargs)
        event = EventPage.objects.get(id=event_id)
        self.fields['featured_price'].initial = event.price
        self.fields['featured_price'].widget.attrs['readonly'] = True
        self.fields['event_page'].initial = event.id
        self.fields['event_page'].widget.attrs['readonly'] = True
        if user:
            self.fields['name'].initial = user.get_full_name()
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['email'].initial = user.email
            self.fields['email'].widget.attrs['readonly'] = True

    class Media:
        js = ['js/customer_autocomplete.js']