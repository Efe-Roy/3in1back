from rest_framework import serializers
from .models import PreviousStudyModel
from contratacionAPI.serializers import ProcessTypeSerializer, ResSecTypeSerializer

class PreviousStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousStudyModel
        fields = '__all__'

class PreviousStudySerializer2(serializers.ModelSerializer):
    process = serializers.SerializerMethodField()
    responsible_secretary = serializers.SerializerMethodField()

    class Meta:
        model = PreviousStudyModel
        fields = '__all__'

    def get_process(self, obj):
        return ProcessTypeSerializer(obj.process).data
    
    def get_responsible_secretary(self, obj):
        return ResSecTypeSerializer(obj.responsible_secretary).data