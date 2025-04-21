from django.urls import path
from .views import (
    create_room, delete_room, list_rooms,
    create_booking, delete_booking, list_bookings
)
from . import views

urlpatterns = [
    path("rooms/create", create_room, name="create_room"),
    path("rooms/delete", delete_room, name="delete_room"),
    path("rooms/list", list_rooms, name="list_rooms"),
    path("bookings/create", create_booking, name="create_booking"),
    path("bookings/delete", delete_booking, name="delete_booking"),
    path("bookings/list", list_bookings, name="list_bookings"),
    path("", views.index, name="home"),
]
