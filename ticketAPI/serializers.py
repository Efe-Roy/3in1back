from rest_framework import serializers
from Auth.serializers import UserSerializer

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ("id", "user", "subject", "description", "state", "responsible_secretary", "created_on", "last_update_on")

    def get_user(self, obj):
        return UserSerializer(obj.user).data