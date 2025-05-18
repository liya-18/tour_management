from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import TourPackage, Booking, Profile
from .forms import VendorSignUpForm, TourPackageForm, BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.db.models import Count
from datetime import date
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    today = date.today()
    valid_packages = TourPackage.objects.filter(expiry_date__gte=today)
    top_packages = valid_packages.order_by('-created_at')[:6]
    budget_packages = valid_packages.order_by('price')[:6]
    popular_destinations = (
        valid_packages.values('destination')
        .annotate(count=Count('destination'))
        .order_by('-count')[:5]
    )
    bg_image_url = request.build_absolute_uri(settings.MEDIA_URL + 'tour_images/bg.jpeg')
    return render(request, 'packages/home.html', {
        'top_packages': top_packages,
        'budget_packages': budget_packages,
        'popular_destinations': popular_destinations,
        'bg_image_url': bg_image_url,
    })

def package_list(request):
    today = timezone.now().date()
    tours = TourPackage.objects.filter(is_approved=True, is_expired=False, expiry_date__gte=today)
    destination = request.GET.get('destination')
    price_sort = request.GET.get('price')
    search_query = request.GET.get('q')
    tag = request.GET.get('tag')

    if destination:
        tours = tours.filter(destination__icontains=destination)
    if search_query:
        tours = tours.filter(name__icontains=search_query)
    if price_sort == 'low':
        tours = tours.order_by('price')
    elif price_sort == 'high':
        tours = tours.order_by('-price')

    return render(request, 'packages/packages.html', {'tours': tours})

def tour_page(request):
    return render(request, 'packages/tour.html')

def package_detail(request, pk):
    tour = get_object_or_404(TourPackage, pk=pk, is_approved=True)
    is_expired = tour.is_expired
    return render(request, 'packages/package_detail.html', {
        'tour': tour,
        'is_expired': is_expired
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                profile = user.profile
            except ObjectDoesNotExist:
                profile = Profile.objects.create(user=user)
            return redirect('login')  # Redirect to login page
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def vendor_dashboard(request):
    try:
        vendor = request.user.vendor
    except:
        return redirect('home')
    packages = TourPackage.objects.filter(vendor=vendor)
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES)
        if form.is_valid():
            tour_package = form.save(commit=False)
            tour_package.vendor = vendor
            tour_package.save()
            return redirect('vendor_dashboard')
    else:
        form = TourPackageForm()
    return render(request, 'packages/vendor_dashboard.html', {
        'form': form,
        'packages': packages
    })

def vendor_register(request):
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                profile = user.profile
            except ObjectDoesNotExist:
                profile = Profile.objects.create(user=user)
            login(request, user)
            return redirect('vendor_dashboard')
    else:
        form = VendorSignUpForm()
    return render(request, 'packages/vendor_register.html', {'form': form})

@login_required
def edit_package(request, pk):
    package = get_object_or_404(TourPackage, pk=pk, vendor__user=request.user)
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = TourPackageForm(instance=package)
    return render(request, 'packages/edit_package.html', {'form': form})

@login_required
def delete_package(request, pk):
    package = get_object_or_404(TourPackage, pk=pk, vendor__user=request.user)
    if request.method == 'POST':
        package.delete()
        return redirect('vendor_dashboard')
    return render(request, 'packages/confirm_delete.html', {'package': package})

@login_required
def book_package(request, pk):
    package = get_object_or_404(TourPackage, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.package = package
            booking.save()
            return redirect('fake_payment', booking.id)
    else:
        form = BookingForm()
    return render(request, 'packages/book_package.html', {
        'form': form,
        'package': package
    })

@login_required
def booking_history(request):
    user = request.user
    bookings = Booking.objects.filter(user=user).order_by('-booking_date')
    return render(request, 'packages/booking_history.html', {'bookings': bookings})

@login_required
def vendor_bookings(request):
    try:
        vendor = request.user.vendor
    except:
        return HttpResponseForbidden("You are not registered as a vendor.")
    bookings = Booking.objects.filter(package__vendor=vendor)
    return render(request, 'packages/vendor_bookings.html', {'bookings': bookings})

@login_required
def booking_success(request):
    return render(request, 'packages/booking_success.html')

@login_required
def fake_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.payment_status = 'Paid'
        booking.save()
        return redirect('payment_success')
    return render(request, 'packages/fake_payment.html', {'booking': booking})

def payment_success(request):
    return render(request, 'packages/payment_success.html')

@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_packages = TourPackage.objects.count()
    total_bookings = Booking.objects.count()
    pending_packages = TourPackage.objects.filter(is_approved=False)
    return render(request, 'packages/admin_dashboard.html', {
        'total_users': total_users,
        'total_packages': total_packages,
        'total_bookings': total_bookings,
        'pending_packages': pending_packages,
    })

@staff_member_required
def approve_package(request, pk):
    package = get_object_or_404(TourPackage, pk=pk)
    package.is_approved = True
    package.save()
    return redirect('admin_dashboard')

@staff_member_required
def delete_package_admin(request, pk):
    package = get_object_or_404(TourPackage, pk=pk)
    package.delete()
    return redirect('admin_dashboard')

def expired_packages(request):
    expired = TourPackage.objects.filter(is_expired=True)
    return render(request, 'packages/expired_packages.html', {'expired_packages': expired})

@staff_member_required
def enhanced_admin_dashboard(request):
    users = User.objects.all()
    profiles = Profile.objects.select_related('user')
    packages = TourPackage.objects.all()
    return render(request, 'packages/admin_panel.html', {
        'users': users,
        'profiles': profiles,
        'packages': packages,
    })

@staff_member_required
def toggle_package_approval(request, package_id):
    package = get_object_or_404(TourPackage, id=package_id)
    package.is_approved = not package.is_approved
    package.save()
    return redirect('enhanced_admin_dashboard')
