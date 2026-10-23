
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from chat.models import ChatRoom

@login_required
def home_view(request):
    rooms = (
        ChatRoom.objects.filter(members=request.user)
        .select_related("created_by").distinct())
    
    return render(request,"core/home.html",{"user":request.user,
                                            "rooms":rooms},)