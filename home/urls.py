from django.contrib import admin
from django.urls import path
from home import views
from home.views import MovieListView, book_showtime, movie_detail
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.index, name="home"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("contact", views.contact, name="contact"),
    path("logout", views.logout, name="logout"),
    path("eventpage/<str:id>", views.eventpage, name="eventpage"),
    path('movie/', MovieListView.as_view(), name='movie-list'),
    path('movie/<int:pk>/', views.movie_detail, name='movie-detail'),
    path('moviebook/<int:showtime_id>/', book_showtime, name='book-showtime'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('charge/', views.charge, name='charge')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)