from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Booking, Gallery
import json


@login_required
def profile_view(request):
    # Fetch all bookings for the logged-in user, newest first
    my_bookings = Booking.objects.filter(user=request.user).order_by('-date')
    
    # Optional: Fetch images uploaded by this user
    my_uploads = Gallery.objects.filter(user=request.user)
    
    context = {
        'bookings': my_bookings,
        'booking_count': my_bookings.count(),
        'uploads': my_uploads
    }
    return render(request, 'profile.html', {'bookings': my_bookings})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
def home(request):
    # This renders the main HTML page
    return render(request, 'index.html')

def get_booked_slots(request):
    # Replaces app.get("/api/bookings")
    date = request.GET.get('date')
    slots = list(Booking.objects.filter(date=date).values_list('slot', flat=True))
    return JsonResponse(slots, safe=False)

def create_booking(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Booking.objects.create(
            # This line ensures the booking is linked to the logged-in person
            user=request.user if request.user.is_authenticated else None,
            name=data['name'],
            phone=data['phone'],
            date=data['date'],
            slot=data['slot']
        )
        return JsonResponse({'status': 'success'})

def get_gallery(request):
    # Fetch all images from the database
    images = Gallery.objects.all().order_by('-created_at')
    data = [
        {
            'id': img.id, 
            'image_url': img.image.url, 
            'caption': img.caption
        } for img in images
    ]
    return JsonResponse(data, safe=False)

def upload_to_gallery(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        caption = request.POST.get('caption', '')
        booking_id = request.POST.get('booking_id') # Ensure this matches your JS key

        Gallery.objects.create(
            user=request.user,
            booking_id=booking_id, # This will now work after the migration
            image=image_file,
            caption=caption
        )
        return JsonResponse({'status': 'success'})