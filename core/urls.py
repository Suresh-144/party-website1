from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Core Pages
    path('', views.home, name='home'),
    path('profile/', views.profile_view, name='profile'),
    
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Booking API
    path('api/bookings/', views.get_booked_slots, name='get_slots'),
    path('api/bookings/create/', views.create_booking, name='create_booking'),
    
    # Gallery API
    path('api/gallery/', views.get_gallery, name='get_gallery'),
    path('api/gallery/upload/', views.upload_to_gallery, name='upload_gallery'),
]

# This is essential for viewing uploaded gallery photos in your profile
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)