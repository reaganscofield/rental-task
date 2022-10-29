import datetime
from django.test import TestCase, RequestFactory
from rental.models import Rental, Reservation
from rental.views.reservation import ReservationView

def createRental(name):
    return Rental.objects.create(name=name)

def createReservation(rental_instance, checkin, checkout):
    return Reservation.objects.create(
        rental_id=rental_instance,
        checkin=datetime.datetime.strptime(f"{checkin} 08:15:27.243860", '%Y-%m-%d %H:%M:%S.%f'),
        checkout=datetime.datetime.strptime(f"{checkout} 08:15:27.243860", '%Y-%m-%d %H:%M:%S.%f'),
    )

def setupView(view, request, *args, **kwargs):
    view.request = request 
    view.args = args, 
    view.kwargs = kwargs
    return view

class ReservationViewTestCase(TestCase):
    factory = RequestFactory()
    request = factory.get('/rental')
    resevationView = setupView(ReservationView(), request)

    def setUp(self):
        print("======================= Testing Reservation View's Methods ==========================")

    def testGetQuerySet(self, **kwargs):
        print("###################################")
        print("Testing GetQuerySet method........ ")
        self.assertQuerysetEqual(self.resevationView.get_queryset(), Reservation.objects.all())
        print("GetQuerySet Case Passed", "\n")

    def testGetContextData(self, **kwargs):
        print("###################################")
        print("Testing GetContextData method........ ")
        self.assertQuerysetEqual(self.resevationView.get_context_data()['reservations'], Reservation.objects.all())
        print("GetContextData Case Passed", "\n")

class ReservationDBTransactionTestCase(TestCase):
    def setUp(self):
        print("======================= Rental #1 ==========================")
        print("###################################")
        print("Crating Rental #1 .............. ")
        createdRental_1 = createRental("Rental")
        print("done", createdRental_1, "\n")

        print("###################################")
        print("Crating Reservation #1 For Rental #1 .............. ")
        createdReservation_1 = createReservation(createdRental_1, "2022-01-01", "2022-01-13")
        print("Done", createdReservation_1, "\n")

        print("###################################")
        print("Crating Reservation #2 For Rental #1 .............. ")
        createdReservation_2 = createReservation(createdRental_1, "2022-01-20", "2022-02-10")
        print("Done", createdReservation_2, "\n")

        print("###################################")
        print("Crating Reservation #3 For Rental #1 .............. ")
        createdReservation_3 = createReservation(createdRental_1, "2022-02-20", "2022-03-10")
        print("Done", createdReservation_3, "\n")

        print("======================= Rental #2 ==========================")

        print("###################################")
        print("Crating Rental #2 .............. ")
        createdRental_2 = createRental("Rental")
        print("done", createdRental_2, "\n")

        print("###################################")
        print("Crating Reservation #4 For Rental #2 .............. ")
        createdReservation_4 = createReservation(createdRental_2, "2022-01-02", "2022-01-20")
        print("Done", createdReservation_4, "\n")

        print("###################################")
        print("Crating Reservation #5 For Rental #2 .............. ")
        createdReservation_5 = createReservation(createdRental_2, "2022-01-20", "2022-02-11")
        print("Done", createdReservation_5, "\n")

    def testResevationsCase(self):
        print("Testing Reservation Cases .............. ")
        reservations = Reservation.objects.all()
        for reservation in Reservation.objects.all():
            if (str(reservation) == "Res-1 ID"): 
                self.assertEqual(reservation.find_previous_reservation(), "-"),
                print(reservation, "------------>", reservation.find_previous_reservation(), "Case Passed")
            if (str(reservation) == "Res-2 ID"):
                self.assertEqual(reservation.find_previous_reservation(), "Res-1 ID"), 
                print(reservation, "------------>", reservation.find_previous_reservation(), "Case Passed")
            if (str(reservation) == "Res-3 ID"):
                self.assertEqual(reservation.find_previous_reservation(), "Res-2 ID"), 
                print(reservation, "------------>", (reservation.find_previous_reservation()), "Case Passed")
            if (str(reservation) == "Res-4 ID"):
                self.assertEqual(reservation.find_previous_reservation(), "-"), 
                print(reservation, "------------>", reservation.find_previous_reservation(), "Case Passed")
            if (str(reservation) == "Res-5 ID"):
                self.assertEqual(reservation.find_previous_reservation(), "Res-4 ID"), 
                print(reservation, "------------>", reservation.find_previous_reservation(), "Case Passed", "\n")
        self.assertEqual(reservations.count(), 5)

