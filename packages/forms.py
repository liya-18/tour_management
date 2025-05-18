from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TourPackage, Vendor
from .models import Booking

# 1. Form for vendors to create/edit tour packages
class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = ['name', 'destination', 'description', 'duration', 'price', 'image']

# 2. Vendor registration form (extends UserCreationForm)
class VendorSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)  # Add this line

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Vendor.objects.create(user=user, company_name=self.cleaned_data['company_name'])
        return user

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['num_people', 'travel_date']