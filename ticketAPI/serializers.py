from rest_framework import serializers
from Auth.serializers import UserSerializer
from Auth.models import TicketUserAgent
from .models import Ticket

class TicketAgentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = TicketUserAgent
        fields = ('id', 'user')

    def get_user(self, obj):
        return UserSerializer(obj.user).data
    
class TicketSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    assign_to_agent = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ("id", "user", "subject", "description", "state", "assign_to_agent", "image", "created_on", "last_update_on")

    def get_user(self, obj):
        return UserSerializer(obj.user).data
    def get_assign_to_agent(self, obj):
        return TicketAgentSerializer(obj.assign_to_agent).data