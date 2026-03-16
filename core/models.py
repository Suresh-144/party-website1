from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    date = models.DateField()
    slot = models.IntegerField()  # Stores hours 9-22
    created_at = models.DateTimeField(auto_now_add=True)

class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    booking = models.ForeignKey('Booking', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='party_gallery/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)