# core/urls.py
from django.urls import path
from . import views  # This works here because views.py is in the same folder

urlpatterns = [
    path('', views.home, name='home'),
    path('api/bookings/', views.get_booked_slots, name='get_slots'),
    path('api/bookings/create/', views.create_booking, name='create_booking'),
    path('api/gallery/', views.get_gallery, name='get_gallery'),
    path('api/gallery/upload/', views.upload_to_gallery, name='upload_gallery'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]