"""
URL configuration for booking_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# booking_app/urls.py
from django.urls import path
from booking_app.views import (

    RegisterView, CustomLoginView, DashboardView, ShowsListView, BookShowView,
    CartView, RemoveFromCartView, CheckoutView, BookingHistoryView,
    ConfirmBookingView, CancelBookingView,LoginView, LogoutView,
    AdminDashboardView, AdminShowsView, AddShowView, EditShowView,
    DeleteShowView, AdminBookingsView, AdminConfirmBookingView,
    AdminCancelBookingView
)

urlpatterns = [
    # User URLs
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('shows/', ShowsListView.as_view(), name='shows'),
    path('book-show/<int:show_id>/', BookShowView.as_view(), name='book-show'),
    path('cart/', CartView.as_view(), name='cart'),
    path('remove-from-cart/<int:show_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('booking-history/', BookingHistoryView.as_view(), name='booking-history'),
    path('confirm-booking/<int:booking_id>/', ConfirmBookingView.as_view(), name='confirm-booking'),
    path('cancel-booking/<int:booking_id>/', CancelBookingView.as_view(), name='cancel-booking'),

    # Admin URLs
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin/shows/', AdminShowsView.as_view(), name='admin-shows'),
    path('admin/shows/add/', AddShowView.as_view(), name='add-show'),
    path('admin/shows/edit/<int:pk>/', EditShowView.as_view(), name='edit-show'),
    path('admin/shows/delete/<int:pk>/', DeleteShowView.as_view(), name='delete-show'),
    path('admin/bookings/', AdminBookingsView.as_view(), name='admin-bookings'),
    path('admin/bookings/confirm/<int:booking_id>/', AdminConfirmBookingView.as_view(), name='admin-confirm-booking'),
    path('admin/bookings/cancel/<int:booking_id>/', AdminCancelBookingView.as_view(), name='admin-cancel-booking'),
]