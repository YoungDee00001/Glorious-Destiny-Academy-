from django.contrib import admin
from .models import ChatRoom, Message, TeacherAssignment
from accounts.models import User


admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(TeacherAssignment)
