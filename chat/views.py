
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from .models import ChatRoom, Message
from .forms import ChatRoomForm, MessageForm

User = get_user_model()

@login_required
def create_room_view(request):
    if request.method == "POST":
        form = ChatRoomForm(request.POST)

        if form.is_valid():
            room = form.save(commit=False)
            room.created_by = request.user
            room.save()
            room.members.add(request.user)

            return redirect("home")
    else:
        form = ChatRoomForm()

    return render(
        request,
        "chat/create_room.html",
        {"form": form},
    )
@login_required
def room_detail_view(request,room_id):
    room =get_object_or_404(ChatRoom.objects.filter(members=request.user),pk=room_id)

    if request.method=="POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message =form.save(commit=False) 
            message.room =room 
            message.sender =request.user
            message.save()
            return redirect("room_detail",room_id=room.id)
    else:
        form =MessageForm()
    chat_messages = list(Message.objects.filter(room=room).select_related("sender").order_by("-created_at","-id")[:100])
    chat_messages.reverse()
    return render(request, "chat/room_detail.html",{
        "room":room,
        "chat_messages":chat_messages,
        "form":form,
    },)

@login_required
def add_room_member_view(request, room_id):
    room = get_object_or_404(
        ChatRoom,
        pk=room_id,
        created_by=request.user,
    )

    if request.method == "POST":
        user_id = request.POST.get("user_id")

        if not user_id:
            messages.error(request, "Please select a user.")
            return redirect("room_detail", room_id=room.id)

        member = get_object_or_404(User, pk=user_id)

        if room.members.filter(pk=member.pk).exists():
            messages.info(request, "This user is already a room member.")
        else:
            room.members.add(member)
            messages.success(request, "User added to the room successfully.")

        return redirect("room_detail", room_id=room.id)

    available_users = User.objects.exclude(
        pk__in=room.members.values_list("pk", flat=True)
    ).exclude(pk=request.user.pk)

    return render(
        request,
        "chat/add_room_member.html",
        {
            "room": room,
            "available_users": available_users,
        },
    )