# packages/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

class TourPackage(models.Model):
    name = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='tour_images/', null=True, blank=True)
    description = models.TextField(blank=True)
    duration = models.CharField(max_length=100, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    is_approved = models.BooleanField(default=False) 
    expiry_date = models.DateField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateField(default="2025-06-01")
    num_people = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ], default='Pending')

    payment_status = models.CharField(max_length=10, choices=[
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    ], default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.package.name} - {self.status}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_vendor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
      if created:
        Profile.objects.get_or_create(user=instance)