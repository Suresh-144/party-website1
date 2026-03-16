from django.contrib import admin
from .models import Booking, Gallery

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # This displays these columns in the admin list view
    list_display = ('date', 'slot', 'user', 'name', 'phone')
    # Adds a filter sidebar
    list_filter = ('date', 'slot')
    # Adds a search bar
    search_fields = ('name', 'phone', 'user__username')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('caption', 'user', 'created_at')