from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import comment

from home.models import Contact
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from home.models import EventPage, Contact
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie, Theater, Showtime, Booking
from .forms import BookingForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, request, JsonResponse
from .models import Booking
from django.urls import reverse
from django.core.mail import send_mail
import requests, stripe
from EventsForU import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from_email = settings.EMAIL_HOST_USER

stripe.api_key = settings.STRIPE_SECRET_KEY


class MovieListView(ListView):
    model = Movie
    template_name = 'movie_list.html'
    context_object_name = 'movies'


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    theaters = Theater.objects.all()
    show = Showtime.objects.filter(movie__id=movie.id)
    return render(request, 'movie_detail.html', {'movie': movie, 'theaters': theaters, "showtime": show})


@login_required
def book_showtime(request, showtime_id):
    showtime = get_object_or_404(Showtime, pk=showtime_id)

    if request.method == 'POST':
        print("Hello World")
        form = BookingForm(request.POST)
        print(f"Form is {form.is_valid()}")
        if form.is_valid():
            print("Hello")
            seats = request.POST.getlist('seats')
            total_price = showtime.movie.price * len(seats)
            booking = form.save(commit=False)
            booking.showtime = showtime
            booking.movie = showtime.movie
            booking.user = request.user
            booking.total_price = total_price
            booking.seats = int(seats[0])
            booking.save()
            print('booking created:', booking.id)
            request.session['booking_data'] = \
                {
                    'movie_id': showtime.movie.id,
                    'movie_name': showtime.movie.title,
                    'showtime': showtime.time.strftime('%Y-%m-%d %H:%M:%S'),
                    'showtime_id': showtime.id,
                    'seats': seats,

                }
            return redirect(reverse('payment', args=[booking.id]))
        else:
            print(form.errors)

    form = BookingForm()
    return render(request, 'book_showtime.html', {'form': form, 'showtime': showtime, 'movie': showtime.movie})


#    if request.method == 'POST':
#        form = BookingForm(request.POST)
#        if form.is_valid():
#            booking = form.save(commit=False)
#            booking.showtime = showtime
#            booking.user = request.user
#            booking.save()
#            messages.success(request,
#                             f'Thank you for booking {booking.seats} seats for {showtime.movie.title} on {showtime.date} at {showtime.time} at {showtime.theater.name}!')
#            return redirect('movie-detail', pk=showtime.movie.pk)
#    else:
#        form = BookingForm()
#    return render(request, 'book_showtime.html', {'form': form, 'showtime': showtime, 'movie': showtime.movie})

def index(request):
    events = EventPage.objects.all()
    contact = Contact.objects.values()
    return render(request, 'index.html', {'events': events, 'contact': contact})


def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if username is not None and password is not None:
            if user is not None:
                auth.login(request, user)
                messages.info(request, "Successfully logged in!")
                return redirect('home')
            else:
                messages.info(request, "invalid credentials")
                return redirect('home')
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':  # fetching the data from form
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already in use')
            return redirect('home')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username already in use')
            return redirect('home')
        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname)
            user.save()
            messages.info(request, 'Successfully Registered. You can now login to your account.')
            return redirect('home')
    else:
        return render(request, "login.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('textbox')
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if result['success']:
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            messages.success(request,
                             'Your response has been sent! You will soon be recieving an email containing all the details. If you cannot find the email in your inbox, check the bulk or the junk folders.')
            event = EventPage.objects.get(id=desc)
            context = {
                "name": name,
                "phone": phone,
                "event": event.title,
                "location": event.location,
                "desc": event.desc,
                "organizer": event.organizer
            }
            message = render_to_string('email/registration_complete_email.html', context)
            send_mail('Registration Completed | EventsForU', strip_tags(message), 'adityaashvin02@gmail.com', [email],
                      fail_silently=False, html_message=message)
            return redirect('home')
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('contact')
    else:
        return render(request, "contact.html")


def eventpage(request, id):
    events = EventPage.objects.filter(id=id).first()
    return render(request, 'eventpage.html', {'events': events})


def logout(request):
    auth.logout(request)
    return redirect('/')


stripe.api_key = settings.STRIPE_SECRET_KEY


def payment(request, booking_id):
    print(booking_id)
    booking_data = request.session.get('booking_data', None)

    # If the booking data is not found, redirect the user back to the movie booking page
    if not booking_data:
        return redirect('book_movie')

    # Get the movie and showtime objects
    movie = Movie.objects.get(pk=booking_data['movie_id'])
    showtime = Showtime.objects.get(pk=booking_data['showtime_id'])
    print(movie)
    # Calculate the total amount to charge
    price_per_seat = movie.price  # Or whatever price you want to charge
    total_amount = price_per_seat * int(booking_data['seats'][0])
    print(int(booking_data['seats'][0]))
    print(settings.STRIPE_PUBLISHABLE_KEY)
    # Render the payment page with the necessary data
    return render(request, 'payment.html', {
        'booking_id': booking_id,
        'movie': movie,
        'showtime': showtime,
        'seats': int(booking_data['seats'][0]),
        'total_amount': total_amount,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })


YOUR_DOMAIN = 'http://127.0.0.1:8080'


def charge(request):
    print(request.POST)
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        print('Booking ID:', booking_id)
        booking = Booking.objects.get(id=booking_id)
        total_amount = int(request.POST.get('total_amount'))
        seats = request.POST.get('seats')
        showtime = booking.showtime
        movie_title = booking.showtime.movie.title

        stripe_token = request.POST.get('stripeToken')
        print(stripe_token)

        try:

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'cad',
                        'product_data': {
                            'name': 'Movie Ticket',
                        },
                        'unit_amount': int(total_amount * 100),
                    },
                    'quantity': seats,
                }],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success.html',
                cancel_url=YOUR_DOMAIN + '/cancel.html',
            )
            print("total_amount",total_amount)
            booking.payment_status = True
            booking.total_price = total_amount
            booking.save()
            messages.success(request,
                             f'Thank you for booking {seats} seats for {movie_title}  at {booking.showtime.time} at {booking.showtime.theater.name}!')
            return redirect('home')
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'})
