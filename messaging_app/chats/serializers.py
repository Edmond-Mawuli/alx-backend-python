from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    # Explicit CharField usage
    phone_number = serializers.CharField(required=True)
    full_name = serializers.SerializerMethodField()  # 👈 computed field

    class Meta:
        model = User
        fields = ["user_id", "username", "first_name", "last_name",
                  "email", "phone_number", "full_name"]

    def get_full_name(self, obj):
        """Return user's full name."""
        return f"{obj.first_name} {obj.last_name}".strip()

    def validate_phone_number(self, value):
        """Ensure phone number is unique."""
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "participant_count"]

    def get_participant_count(self, obj):
        """Return number of participants in the conversation."""
        return obj.participants.count()


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["message_id", "conversation", "sender",
                  "message_body", "sent_at"]
