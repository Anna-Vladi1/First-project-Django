import pytest
from django.urls import reverse
from django.test import Client
from rooms_app.models import Room, Booking

@pytest.mark.django_db
def test_create_room():
    client = Client()
    response = client.post(
        reverse('create_room'),
        data={'description': 'Test Room', 'price_per_night': '100'}
    )
    assert response.status_code == 201
    json_data = response.json()
    assert 'room_id' in json_data

@pytest.mark.django_db
def test_create_booking():
    client = Client()

    # Сначала создаём номер
    room = Room.objects.create(description="Test Room", price_per_night=100)

    # Создаём бронь через POST-запрос
    response = client.post(
        reverse("create_booking"),
        data={
            "room_id": room.id,
            "date_start": "2025-06-01",
            "date_end": "2025-06-05",
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert "booking_id" in data

    # Проверим, что бронь реально создалась
    booking = Booking.objects.get(id=data["booking_id"])
    assert booking.room == room
    assert str(booking.date_start) == "2025-06-01"

@pytest.mark.django_db
def test_booking_date_overlap_not_allowed():
    client = Client()
    room = Room.objects.create(description="Overlap Room", price_per_night=150)

    # Первая бронь с 10 по 15 июня
    Booking.objects.create(room=room, date_start="2025-06-10", date_end="2025-06-15")

    # Пытаемся забронировать с 13 по 17 июня — ДОЛЖНО БЫТЬ ОТКАЗАНО
    response = client.post(
        reverse("create_booking"),
        data={
            "room_id": room.id,
            "date_start": "2025-06-13",
            "date_end": "2025-06-17",
        }
    )

    assert response.status_code == 400
    assert "not available" in response.json()["error"]

@pytest.mark.django_db
def test_list_bookings_sorted_by_start_date():
    client = Client()
    room = Room.objects.create(description="Room with bookings", price_per_night=200)

    Booking.objects.create(room=room, date_start="2025-07-10", date_end="2025-07-15")
    Booking.objects.create(room=room, date_start="2025-06-01", date_end="2025-06-05")

    response = client.get(reverse("list_bookings"), data={"room_id": room.id})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["date_start"] == "2025-06-01"  # раньше
    assert data[1]["date_start"] == "2025-07-10"  # позже

@pytest.mark.django_db
def test_delete_room_also_deletes_bookings():
    client = Client()
    room = Room.objects.create(description="Deletable room", price_per_night=300)

    Booking.objects.create(room=room, date_start="2025-08-01", date_end="2025-08-03")
    Booking.objects.create(room=room, date_start="2025-08-10", date_end="2025-08-12")

    assert Booking.objects.count() == 2

    response = client.post(
        reverse("delete_room"),
        data={"room_id": room.id}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Room deleted"

    # Все бронирования тоже должны исчезнуть
    assert Booking.objects.count() == 0
