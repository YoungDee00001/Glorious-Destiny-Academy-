from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL  # still correct

class TeacherAssignment(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_parents',
        limit_choices_to={'teacher_profile__isnull': False}  # ✅ filter by teacher_profile
    )
    parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_teachers',
        limit_choices_to={'parent_profile__isnull': False}  # ✅ filter by parent_profile
    )

    def __str__(self):
        return f"{self.teacher.username} <-> {self.parent.username}"

class ChatRoom(models.Model):
    parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='parent_rooms',
        limit_choices_to={'parent_profile__isnull': False}  # ✅ filter by parent_profile
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_rooms',
        limit_choices_to={'teacher_profile__isnull': False}  # ✅ filter by teacher_profile
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.parent.username} & {self.teacher.username}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
