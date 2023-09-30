from rest_framework import serializers
from .models import SisbenMain, LocationType


class LocationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationType
        fields = '__all__'

class SisbenMainSerializer2(serializers.ModelSerializer):
    class Meta:
        model = SisbenMain
        fields = '__all__'

class SisbenMainSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    class Meta:
        model = SisbenMain
        fields = ('id', 'citizenship_card', 'full_name', 'cell_phone', 'location')

    def get_location(self, obj):
        return LocationTypeSerializer(obj.location).data
    
