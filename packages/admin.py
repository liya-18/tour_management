from django.contrib import admin
from .models import Profile, TourPackage, Booking

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
   list_display = ('user', 'is_vendor', 'is_admin')  
   list_filter = ('is_vendor', 'is_admin') 

admin.site.register(TourPackage)
admin.site.register(Booking)
