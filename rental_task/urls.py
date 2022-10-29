from django.contrib import admin
from django.urls import path, include
from rental.views.reservation import ReservationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rental/', ReservationView.as_view(),  name='reservation_view'),
]