from django.db import models
from django.contrib.auth.models import User

class Show(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=100)
    total_seats = models.IntegerField()

    def __str__(self):
        return f"{self.name} at {self.venue} on {self.date}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user} for {self.show}"

class BookedSeat(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    seat_number = models.IntegerField()

    class Meta:
        unique_together = [('show', 'seat_number')]

    def __str__(self):
        return f"Seat {self.seat_number} for {self.show}"