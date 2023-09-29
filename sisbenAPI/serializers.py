from rest_framework import serializers
from .models import SisbenMain


class SisbenMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = SisbenMain
        fields = '__all__'

