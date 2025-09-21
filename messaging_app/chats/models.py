from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


# Custom User model
class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)  # This replaces the default `id`
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    user_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Django hashes this internally
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# Conversation model
class Conversation(models.Model):
    conversation_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# Message model
class Message(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="messages_sent", on_delete=models.CASCADE)
    message_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} by {self.sender}"
