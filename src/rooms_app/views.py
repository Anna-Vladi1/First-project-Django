import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .models import Room, Booking

@csrf_exempt
def create_room(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        price_str = request.POST.get('price_per_night')

        if not description or not price_str:
            return JsonResponse({"error": "Missing parameters"}, status=400)

        try:
            price = float(price_str)
        except ValueError:
            return JsonResponse({"error": "price_per_night must be numeric"}, status=400)

        room = Room.objects.create(
            description=description,
            price_per_night=price
        )
        return JsonResponse({"room_id": room.id}, status=201)

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def delete_room(request):
    if request.method == 'POST':
        room_id_str = request.POST.get('room_id')
        if not room_id_str:
            return JsonResponse({"error": "room_id is required"}, status=400)

        try:
            room_id = int(room_id_str)
            room = Room.objects.get(id=room_id)
        except ValueError:
            return JsonResponse({"error": "room_id must be an integer"}, status=400)
        except Room.DoesNotExist:
            return JsonResponse({"error": "Room not found"}, status=404)

        # Удаляем
        room.delete()
        return JsonResponse({"status": "Room deleted"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

def list_rooms(request):
    if request.method == 'GET':
        sort_by = request.GET.get('sort_by')  # price / date_added
        order = request.GET.get('order', 'asc')

        queryset = Room.objects.all()

        if sort_by in ['price', 'date_added']:
            if sort_by == 'price':
                field_name = 'price_per_night'
            else:
                field_name = 'date_added'

            if order == 'desc':
                field_name = '-' + field_name

            queryset = queryset.order_by(field_name)

        data = []
        for r in queryset:
            data.append({
                "room_id": r.id,
                "description": r.description,
                "price_per_night": str(r.price_per_night),
                "date_added": r.date_added.strftime("%Y-%m-%d %H:%M:%S")
            })
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def create_booking(request):
    if request.method == 'POST':
        room_id_str = request.POST.get('room_id')
        date_start_str = request.POST.get('date_start')
        date_end_str = request.POST.get('date_end')

        if not all([room_id_str, date_start_str, date_end_str]):
            return JsonResponse({"error": "room_id, date_start, date_end are required"}, status=400)

        try:
            room_id = int(room_id_str)
            room = Room.objects.get(id=room_id)
        except ValueError:
            return JsonResponse({"error": "room_id must be integer"}, status=400)
        except Room.DoesNotExist:
            return JsonResponse({"error": "Room not found"}, status=404)

        # Проверяем формат дат
        try:
            date_start = datetime.datetime.strptime(date_start_str, '%Y-%m-%d').date()
            date_end = datetime.datetime.strptime(date_end_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({"error": "Dates must be YYYY-MM-DD"}, status=400)

        if date_start > date_end:
            return JsonResponse({"error": "date_start cannot be after date_end"}, status=400)

        # (Дополнительно) Проверим пересечение дат
        overlap = Booking.objects.filter(room=room).filter(
            date_start__lte=date_end,
            date_end__gte=date_start
        )
        if overlap.exists():
            return JsonResponse({"error": "Room is not available for the given dates"}, status=400)

        booking = Booking.objects.create(room=room, date_start=date_start, date_end=date_end)
        return JsonResponse({"booking_id": booking.id}, status=201)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def delete_booking(request):
    if request.method == 'POST':
        booking_id_str = request.POST.get('booking_id')
        if not booking_id_str:
            return JsonResponse({"error": "booking_id is required"}, status=400)
        try:
            booking_id = int(booking_id_str)
            booking = Booking.objects.get(id=booking_id)
        except ValueError:
            return JsonResponse({"error": "booking_id must be integer"}, status=400)
        except Booking.DoesNotExist:
            return JsonResponse({"error": "Booking not found"}, status=404)

        booking.delete()
        return JsonResponse({"status": "Booking deleted"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

def list_bookings(request):
    if request.method == 'GET':
        room_id_str = request.GET.get('room_id')
        if not room_id_str:
            return JsonResponse({"error": "room_id is required"}, status=400)

        try:
            room_id = int(room_id_str)
            if not Room.objects.filter(id=room_id).exists():
                return JsonResponse({"error": "Room not found"}, status=404)
        except ValueError:
            return JsonResponse({"error": "room_id must be integer"}, status=400)

        bookings = Booking.objects.filter(room_id=room_id).order_by('date_start')
        data = []
        for b in bookings:
            data.append({
                "booking_id": b.id,
                "date_start": b.date_start.strftime("%Y-%m-%d"),
                "date_end": b.date_end.strftime("%Y-%m-%d")
            })
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

def index(request):#главная страница
    return HttpResponse("Hello! This is the root page.")