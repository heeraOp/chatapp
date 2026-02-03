from django.db import models

class ChatUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.username


class Message(models.Model):
    room = models.CharField(max_length=100)
    user = models.ForeignKey(
        ChatUser,
        on_delete=models.CASCADE,
        null=True,      # ✅ TEMPORARY
        blank=True
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
