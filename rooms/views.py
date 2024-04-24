from django.shortcuts import render
from .models import Room


# Create your views here.
def see_rooms(request):
    rooms = Room.objects.all()
    return render(
        request,
        "rooms.html",
        {
            "rooms": rooms,
            "title": "Rooms",
        },
    )


def see_room(request, room_pk):
    try:
        room = Room.objects.get(pk=room_pk)
        return render(
            request,
            "room.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist:
        return render(
            request,
            "room.html",
            {
                "not_found": True,
            },
        )
