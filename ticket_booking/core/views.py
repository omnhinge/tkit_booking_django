from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView
from django.db import transaction, IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from .models import Show, Booking, BookedSeat
from django.shortcuts import render

def home(request):
    return render(request, 'base.html')  # Create a home.html template for the home page

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if not username or not password or not email:
            messages.error(request, 'All fields are required.')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        messages.success(request, 'Registration successful.')
        return redirect('show_list')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('show_list')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')

class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('login')

class ShowListView(ListView):
    model = Show
    template_name = 'show_list.html'
    context_object_name = 'shows'

class ShowDetailView(View):
    def get(self, request, pk):
        show = Show.objects.get(pk=pk)
        booked_seats = BookedSeat.objects.filter(show=show).values_list('seat_number', flat=True)
        available_seats = [i for i in range(1, show.total_seats + 1) if i not in booked_seats]
        return render(request, 'show_detail.html', {'show': show, 'available_seats': available_seats})

    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to book tickets.')
            return redirect('login')
        show = Show.objects.get(pk=pk)
        selected_seats = request.POST.getlist('seats')
        selected_seats = [int(seat) for seat in selected_seats]
        booked_seats = BookedSeat.objects.filter(show=show).values_list('seat_number', flat=True)
        available_seats = [i for i in range(1, show.total_seats + 1) if i not in booked_seats]
        if not all(seat in available_seats for seat in selected_seats):
            messages.error(request, 'Some selected seats are not available.')
            return redirect('show_detail', pk=pk)
        try:
            with transaction.atomic():
                booking = Booking.objects.create(user=request.user, show=show)
                for seat in selected_seats:
                    BookedSeat.objects.create(show=show, booking=booking, seat_number=seat)
            messages.success(request, 'Booking successful.')
            return redirect('booking_list')
        except IntegrityError:
            messages.error(request, 'Some seats were booked by someone else. Please try again.')
            return redirect('show_detail', pk=pk)

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking_list.html'
    context_object_name = 'bookings'
    login_url = '/login/'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

@method_decorator(staff_member_required, name='dispatch')
class ShowCreateView(View):
    def get(self, request):
        return render(request, 'show_form.html')

    def post(self, request):
        name = request.POST.get('name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        venue = request.POST.get('venue')
        total_seats = request.POST.get('total_seats')
        if not all([name, date, time, venue, total_seats]):
            messages.error(request, 'All fields are required.')
            return redirect('show_create')
        try:
            total_seats = int(total_seats)
        except ValueError:
            messages.error(request, 'Total seats must be an integer.')
            return redirect('show_create')
        Show.objects.create(name=name, date=date, time=time, venue=venue, total_seats=total_seats)
        messages.success(request, 'Show created successfully.')
        return redirect('show_list')

@method_decorator(staff_member_required, name='dispatch')
class ShowUpdateView(View):
    def get(self, request, pk):
        show = Show.objects.get(pk=pk)
        return render(request, 'show_form.html', {'show': show})

    def post(self, request, pk):
        show = Show.objects.get(pk=pk)
        name = request.POST.get('name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        venue = request.POST.get('venue')
        total_seats = request.POST.get('total_seats')
        if not all([name, date, time, venue, total_seats]):
            messages.error(request, 'All fields are required.')
            return redirect('show_update', pk=pk)
        try:
            total_seats = int(total_seats)
        except ValueError:
            messages.error(request, 'Total seats must be an integer.')
            return redirect('show_update', pk=pk)
        show.name = name
        show.date = date
        show.time = time
        show.venue = venue
        show.total_seats = total_seats
        show.save()
        messages.success(request, 'Show updated successfully.')
        return redirect('show_list')

@method_decorator(staff_member_required, name='dispatch')
class ShowDeleteView(View):
    def get(self, request, pk):
        show = Show.objects.get(pk=pk)
        return render(request, 'show_confirm_delete.html', {'show': show})

    def post(self, request, pk):
        show = Show.objects.get(pk=pk)
        show.delete()
        messages.success(request, 'Show deleted successfully.')
        return redirect('show_list')

@method_decorator(staff_member_required, name='dispatch')
class BookingAdminListView(ListView):
    model = Booking
    template_name = 'booking_admin_list.html'
    context_object_name = 'bookings'