# booking_app/views.py
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from .models import Show, Booking, CustomUser
import datetime
from django.utils import timezone
class RegisterView(CreateView):
    model = CustomUser
    template_name = 'register.html'
    fields = ['username', 'email', 'password']
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, 'Registration successful! Please login.')
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Welcome back, {self.request.user.username}!')
        return response

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_shows'] = Show.objects.filter(date_time__gte=timezone.now()).order_by('date_time')[:3]
        context['recent_bookings'] = Booking.objects.filter(user=self.request.user).order_by('-booked_at')[:3]
        return context

class ShowsListView(LoginRequiredMixin, ListView):
    model = Show
    template_name = 'shows.html'
    context_object_name = 'shows'
    queryset = Show.objects.filter(date_time__gte=timezone.now()).order_by('date_time')

class BookShowView(LoginRequiredMixin, View):
    def get(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        return render(request, 'booking.html', {'show': show})

    def post(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        seats = int(request.POST.get('seats', 0))
        
        if seats <= 0 or seats > show.available_seats:
            messages.error(request, 'Invalid number of seats selected.')
            return redirect('book-show', show_id=show_id)
        
        cart = request.session.get('cart', {})
        cart[str(show_id)] = {
            'seats': seats,
            'total_price': float(seats * show.price)
        }
        request.session['cart'] = cart
        messages.success(request, 'Added to cart successfully!')
        return redirect('cart')

class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = request.session.get('cart', {})
        shows = Show.objects.filter(id__in=cart.keys())
        cart_items = []
        total_seats = 0
        total = 0
        
        for show in shows:
            item = cart[str(show.id)]
            cart_items.append({
                'show': show,
                'seats': item['seats'],
                'total_price': item['total_price']
            })
            total_seats += item['seats']
            total += item['total_price']
        
        return render(request, 'cart.html', {
            'cart_items': cart_items,
            'total_seats': total_seats,
            'total': total
        })

class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, show_id):
        cart = request.session.get('cart', {})
        if str(show_id) in cart:
            del cart[str(show_id)]
            request.session['cart'] = cart
            messages.success(request, 'Item removed from cart.')
        return redirect('cart')

class CheckoutView(LoginRequiredMixin, View):
    def post(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, 'Your cart is empty!')
            return redirect('shows')
        
        for show_id, item in cart.items():
            show = Show.objects.get(id=show_id)
            Booking.objects.create(
                user=request.user,
                show=show,
                seats=item['seats'],
                total_price=item['total_price'],
                is_confirmed=True
            )
            show.available_seats -= item['seats']
            show.save()
        
        request.session['cart'] = {}
        messages.success(request, 'Booking confirmed successfully!')
        return redirect('booking-history')

class BookingHistoryView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'history.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booked_at')

class ConfirmBookingView(LoginRequiredMixin, View):
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        booking.is_confirmed = True
        booking.save()
        messages.success(request, 'Booking confirmed!')
        return redirect('booking-history')

class CancelBookingView(LoginRequiredMixin, View):
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        show = booking.show
        show.available_seats += booking.seats
        show.save()
        booking.delete()
        messages.success(request, 'Booking cancelled.')
        return redirect('booking-history')

# Admin Views
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/dashboard.html'

    def test_func(self):
        return self.request.user.is_admin

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_shows'] = Show.objects.count()
        context['total_bookings'] = Booking.objects.count()
        context['total_revenue'] = Booking.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        context['upcoming_shows_count'] = Show.objects.filter(date_time__gte=timezone.now()).count()
        return context

class AdminShowsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Show
    template_name = 'admin/shows.html'
    context_object_name = 'shows'

    def test_func(self):
        return self.request.user.is_admin

class AddShowView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Show
    template_name = 'admin/add_show.html'
    fields = ['title', 'description', 'date_time', 'duration', 'venue', 'total_seats', 'price']
    success_url = reverse_lazy('admin-shows')

    def test_func(self):
        return self.request.user.is_admin

    def form_valid(self, form):
        form.instance.available_seats = form.cleaned_data['total_seats']
        messages.success(self.request, 'Show added successfully!')
        return super().form_valid(form)

class EditShowView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Show
    template_name = 'admin/add_show.html'
    fields = ['title', 'description', 'date_time', 'duration', 'venue', 'total_seats', 'price']
    success_url = reverse_lazy('admin-shows')

    def test_func(self):
        return self.request.user.is_admin

    def form_valid(self, form):
        messages.success(self.request, 'Show updated successfully!')
        return super().form_valid(form)

class DeleteShowView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Show
    success_url = reverse_lazy('admin-shows')

    def test_func(self):
        return self.request.user.is_admin

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Show deleted successfully!')
        return super().delete(request, *args, **kwargs)

class AdminBookingsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Booking
    template_name = 'admin/bookings.html'
    context_object_name = 'bookings'

    def test_func(self):
        return self.request.user.is_admin

class AdminConfirmBookingView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_admin

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        booking.is_confirmed = True
        booking.save()
        messages.success(request, 'Booking confirmed!')
        return redirect('admin-bookings')

class AdminCancelBookingView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_admin

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        show = booking.show
        show.available_seats += booking.seats
        show.save()
        booking.delete()
        messages.success(request, 'Booking cancelled.')
        return redirect('admin-bookings')