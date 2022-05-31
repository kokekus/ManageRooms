from django.shortcuts import render, redirect
from .models import RoomInfo, RoomReservation
from datetime import datetime, timedelta
# Create your views here.
def main_page(request):
    all_rooms = RoomInfo.objects.all()
    reserved_today = RoomInfo.objects.filter(roomreservation__date=datetime.now()).values_list('id', flat=True)
    for room in all_rooms:
        room.available = None if room.id in reserved_today else True
    if request.method == 'GET':
        context = {'rooms': all_rooms}
        return render(request, "index2.html", context)

def search_room(request):
    all_rooms = RoomInfo.objects.all()
    name = request.GET.get("room_name")
    capacity = request.GET.get("capacity")
    capacity = int(capacity) if capacity else 0
    projector_available = request.GET.get("projector") == "on"
    if projector_available:
        all_rooms = all_rooms.filter(projector_available=projector_available)
    if capacity:
        all_rooms = all_rooms.filter(capacity__gte=capacity)
    if name:
        all_rooms = all_rooms.filter(name__contains=name)
    context = {'rooms': all_rooms}
    return render(request, "index2.html", context)




def add_room(request):
    context = {}
    name_error_message = value_error_message = ""
    if request.method == 'POST':
        name = request.POST.get('room_name')
        capacity = request.POST.get('room_capacity')
        projector_available = request.POST.get('projector_available')
        if not name:
            name_error_message = "Room name can't be empty..."
        if RoomInfo.objects.filter(name=name).exists():
            name_error_message = "Room name exists..."
        try:
            if int(capacity) < 1:
                value_error_message = "Room capacity has to be higher than 0..."
        except ValueError:
            value_error_message = "Room capacity has to be higher than 0..."
        if not name_error_message and not value_error_message:
            RoomInfo.objects.create(name=name, capacity=capacity, projector_available=projector_available)
            context['saved_message'] = f'{name} added'
        else:
            context['name'] = name
            context['capacity'] = capacity
            context['projector_available'] = projector_available
            context['name_error_message'] = name_error_message
            context['value_error_message'] = value_error_message
    return render(request, "new_room.html", context)

def delete_room(request, id):
    context = {'id': id,
               }
    if request.method == 'POST':
        RoomInfo.objects.filter(id=id).delete()
        return redirect("/")
    return render(request, "delete_room.html", context)

def modify_room(request, id):
    name_error_message = value_error_message = ""
    room = RoomInfo.objects.filter(id=id).first()
    context = { 'name' : room.name,
                'capacity': room.capacity,
                'projector_available': room.projector_available}
    if request.method == 'POST':
        name = request.POST.get('room_name')
        capacity = request.POST.get('room_capacity')
        projector_available = request.POST.get('projector_available')
        if not name:
            name_error_message = "Room name can't be empty..."
        if RoomInfo.objects.filter(name=name).exists() and name != room.name:
            name_error_message = "Room name exists..."
        try:
            if int(capacity) < 1:
                value_error_message = "Room capacity has to be higher than 0..."
        except ValueError:
            value_error_message = "Room capacity has to be higher than 0..."
        context['name'] = name
        context['capacity'] = capacity
        context['projector_available'] = projector_available
        context['name_error_message'] = name_error_message
        context['value_error_message'] = value_error_message
        projector_available = str(projector_available or 0)
        if not name_error_message and not value_error_message:
            room.name = name
            room.capacity = capacity
            room.projector_available = projector_available
            room.save()
            return redirect("/")
    return render(request, "modify_room.html", context)

def reserve_room(request, id):
    date_error_message = ''
    this_room = RoomInfo.objects.filter(pk=id).first()
    context = {'name': this_room.name,
               'capacity': this_room.capacity,
               'projector_available': this_room.projector_available,
               'id': id}
    if request.method == 'POST':
        comment = request.POST.get('room_comment')
        date = datetime.strptime(request.POST.get('room_date'),'%Y-%m-%d')
        if RoomReservation.objects.filter(room_id=id).filter(date=date).exists():
            date_error_message = 'Room already booked for that date'
        if date < (datetime.now() - timedelta(days=1)):
            date_error_message = 'Please book room for today or the future'
        context['date_error_message'] = date_error_message
        if not date_error_message:
            RoomReservation.objects.create(comment=comment, date=date, room_id_id=int(id))
            return redirect("/")
    return render(request, "reserve_room.html", context)

def view_room(request, id):
    this_room = RoomInfo.objects.filter(pk=id).first()
    reservations = RoomReservation.objects.filter(room_id=id).all()
    context = {'name': this_room.name,
               'capacity': this_room.capacity,
               'projector_available': this_room.projector_available,
               'id': id,
               'reservations': reservations}
    return render(request, "view_room.html", context)
