from django.db import models
from rental.models import Rental

class Reservation(models.Model):
    checkin = models.DateField()
    checkout = models.DateField()
    rental_id = models.ForeignKey(Rental, on_delete=models.CASCADE)
    
    def find_previous_reservation(self):
        latest_reservation = Reservation.objects.order_by('-checkout').filter(
            rental_id=self.rental_id, checkout__lt=self.checkout
        ).first()
        if latest_reservation is not None:
            return f"Res-{latest_reservation.id} ID"
        return '-'

    def __str__(self):
        return f"Res-{self.id} ID"