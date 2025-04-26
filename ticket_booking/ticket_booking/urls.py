"""
URL configuration for ticket_booking project.

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
from django.urls import path
from core.views import (
    RegisterView, LoginView, LogoutView,
    ShowListView, ShowDetailView, BookingListView,
    ShowCreateView, ShowUpdateView, ShowDeleteView,
    BookingAdminListView
)
from . import views
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('shows/', ShowListView.as_view(), name='show_list'),
    path('shows/<int:pk>/', ShowDetailView.as_view(), name='show_detail'),
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('admin/shows/create/', ShowCreateView.as_view(), name='show_create'),
    path('admin/shows/<int:pk>/update/', ShowUpdateView.as_view(), name='show_update'),
    path('admin/shows/<int:pk>/delete/', ShowDeleteView.as_view(), name='show_delete'),
    path('admin/bookings/', BookingAdminListView.as_view(), name='booking_admin_list'),
]
