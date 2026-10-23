
from django.urls import path
from . import views

urlpatterns = [
    path("rooms/create/", views.create_room_view, name="create_room"),
    path("room/<int:room_id>/",views.room_detail_view , name="room_detail"),
    path("rooms/<int:room_id>/members/add/",views.add_room_member_view,name="add_room_member"),
]
