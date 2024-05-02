from rest_framework import serializers
from .models import PreviousStudyModel, OperationModel
from contratacionAPI.serializers import ProcessTypeSerializer, ResSecTypeSerializer
from Auth.serializers import UserSerializer

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
    


class OperationSerializer(serializers.ModelSerializer):
    authorize_user = serializers.SerializerMethodField()

    class Meta:
        model = OperationModel
        fields = '__all__'

    def get_authorize_user(self, obj):
        return UserSerializer(obj.authorize_user).data