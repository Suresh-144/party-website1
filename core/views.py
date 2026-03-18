from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Booking, Gallery
from django.core.mail import send_mail
from django.conf import settings
import json

def send_booking_confirmation(user_email, booking_details):
    """
    Sends a confirmation email using the email passed from the view.
    """
    subject = 'Booking Confirmed - The Party Den'
    message = f'Hi! Your booking for {booking_details.date} at {booking_details.slot}:00 is confirmed.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    
    # fail_silently=False will help you see errors in your terminal during testing
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)

def create_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # 1. Create the booking object in the database
            booking = Booking.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=data['name'],
                phone=data['phone'],
                date=data['date'],
                slot=data['slot']
            )
            
            # 2. Trigger the email if the user is logged in and has an email
            if request.user.is_authenticated and request.user.email:
                try:
                    send_booking_confirmation(request.user.email, booking)
                except Exception as e:
                    # Log SMTP errors without crashing the booking process
                    print(f"Email failed to send: {e}")

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def profile_view(request):
    my_bookings = Booking.objects.filter(user=request.user).order_by('-date')
    my_uploads = Gallery.objects.filter(user=request.user)
    
    context = {
        'bookings': my_bookings,
        'booking_count': my_bookings.count(),
        'uploads': my_uploads
    }
    return render(request, 'profile.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        email = request.POST.get('email')
        if form.is_valid():
            user = form.save(commit=False)
            user.email = email
            user.save()
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
    return render(request, 'index.html')

def get_booked_slots(request):
    date = request.GET.get('date')
    slots = list(Booking.objects.filter(date=date).values_list('slot', flat=True))
    return JsonResponse(slots, safe=False)

def get_gallery(request):
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
        booking_id = request.POST.get('booking_id')

        Gallery.objects.create(
            user=request.user,
            booking_id=booking_id,
            image=image_file,
            caption=caption
        )
        return JsonResponse({'status': 'success'})