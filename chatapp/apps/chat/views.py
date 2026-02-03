from django.shortcuts import render

def index(request):
    """
    Landing page – user enters a room name
    """
    return render(request, "chat/index.html")


def room(request, room):
    """
    Chat room page
    """
    return render(request, "chat/room.html", {
        "room": room
    })
