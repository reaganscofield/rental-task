from rental.models import *
from django.views.generic import TemplateView

class ReservationView(TemplateView):
    fields = '__all__'
    template_name = "reservations.html"
    
    def get_queryset(self):
        return Reservation.objects.all()

    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        context['reservations'] = Reservation.objects.all()
        return context