from django.urls import path
from .views import index, room

urlpatterns = [
    path("", index, name="index"),
    path("chat/<str:room>/", room, name="room"),
]
