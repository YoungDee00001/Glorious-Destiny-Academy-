from django.shortcuts import render, get_object_or_404
from .models import ChatRoom

def chat_list(request):
    user = request.user
    if user.role == 'parent':
        rooms = ChatRoom.objects.filter(parent=user)
    elif user.role == 'teacher':
        rooms = ChatRoom.objects.filter(teacher=user)
    else:
        rooms = ChatRoom.objects.all()
    return render(request, 'chat/chat_list.html', {'rooms': rooms})


def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    messages = room.messages.all().order_by('timestamp')
    return render(request, 'chat/chat_room.html', {
        'room': room,
        'messages': messages
    })
