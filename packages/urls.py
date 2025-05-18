from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('packages/', views.package_list, name='packages'),
    path('tour/', views.home, name='tour'),
    path('register/', views.register, name='register'),
    path('vendor/register/', views.vendor_register, name='vendor_register'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('package/<int:pk>/', views.package_detail, name='package_detail'),
    path('vendor/package/edit/<int:pk>/', views.edit_package, name='edit_package'),
    path('vendor/package/delete/<int:pk>/', views.delete_package, name='delete_package'),
    path('package/<int:pk>/book/', views.book_package, name='book_package'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('vendor/bookings/', views.vendor_bookings, name='vendor_bookings'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/package/<int:pk>/approve/', views.approve_package, name='approve_package'),
    path('expired-packages/', views.expired_packages, name='expired_packages'),
    path('my-bookings/', views.booking_history, name='booking_history'),
    path('payment/<int:booking_id>/', views.fake_payment, name='fake_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('admin-panel/', views.enhanced_admin_dashboard, name='enhanced_admin_dashboard'),
    path('admin-panel/toggle-package/<int:package_id>/', views.toggle_package_approval, name='toggle_package_approval'),
    path('admin/delete-package/<int:pk>/', views.delete_package_admin, name='delete_package_admin'),




]
