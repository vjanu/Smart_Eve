from django.contrib import admin
from django.urls import path
from home import views
from home.views import MovieListView, book_showtime, movie_detail, CancelBookingEvent, CancelBookingMovie, Profile
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.index, name="home"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
   # path("contact", views.contact, name="contact"),
    path("logout", views.logout, name="logout"),
    path("eventpage/<str:id>", views.eventpage, name="eventpage"),
    path('movie/', MovieListView.as_view(), name='movie-list'),
    path('movie/<int:pk>/', views.movie_detail, name='movie-detail'),
    path('moviebook/<int:showtime_id>/', book_showtime, name='book-showtime'),
    path('book_service/<uuid:booking_id>/', views.book_service, name='book_service'),
    path('payment/<uuid:booking_id>/', views.payment, name='payment'),
    path('charge/', views.charge, name='charge'),

    path ( 'booking/<uuid:booking_id>/' , views.booking_detail , name = 'booking_detail' ) ,
    path('booking/<uuid:booking_id>/pdf/', views.booking_pdf, name='booking_pdf'),
    path ( 'bookings/' , views.bookings , name = 'bookings' ) ,
    path('bookings/cancel_bookingmovie', CancelBookingMovie.as_view(), name="cancel_bookingmovie"),
    path('bookings/cancel_bookingevent', CancelBookingEvent.as_view(), name="cancel_bookingevent"),
    path('profile', Profile.as_view(), name="profile"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)