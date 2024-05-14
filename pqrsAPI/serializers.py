from rest_framework import serializers
from .models import PqrsMain, EntityType, NameType, MediumResType, StatusType, PqrsNotifify

from Auth.serializers import TeamSerializer
from Auth.models import Team


class PqrsMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = PqrsMain
        fields = '__all__'

class EntityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityType
        fields = '__all__'

class NameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameType
        fields = '__all__'

class MediumResTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediumResType
        fields = '__all__'

class StatusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusType
        fields = '__all__'

# class StatusTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = '__all__'


class AllPqrsSerializer(serializers.ModelSerializer):
    entity_or_position = serializers.SerializerMethodField()
    status_of_the_response = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    medium_of_the_response = serializers.SerializerMethodField()
    responsible_for_the_response = serializers.SerializerMethodField()

    class Meta:
        model = PqrsMain
        fields = '__all__'
        # fields = (
        #     'id', 'date_of_entry', 'sender', 'entity_or_position', 
        #     'subject', 'file_num', 'responsible_for_the_response', 
        #     'name', 'days_of_the_response', 'expiration_date', 'need_answer',
        #     'status_of_the_response', 'medium_of_the_response', 
        #     'date_of_response', 'file_res', 'comment', 'pdf'
        # )

    def get_entity_or_position(self, obj):
        return EntityTypeSerializer(obj.entity_or_position).data

    def get_status_of_the_response(self, obj):
        return StatusTypeSerializer(obj.status_of_the_response).data

    def get_name(self, obj):
        return NameTypeSerializer(obj.name).data
    
    def get_medium_of_the_response(self, obj):
        return MediumResTypeSerializer(obj.medium_of_the_response).data
    
    def get_responsible_for_the_response(self, obj):
        return TeamSerializer(obj.responsible_for_the_response).data

class InnerFormPqrsMaintSerializer(serializers.ModelSerializer):

    class Meta:
        model = PqrsMain
        # fields = '__all__'
        fields = ( 'id', 'medium_of_the_response', 'status_of_the_response', 'comment', 'file_res', 'pdf', 'pdf_res' )
    

class PqrsNotifySerializer(serializers.ModelSerializer):

    class Meta:
        model = PqrsNotifify
        fields = (
            'id',
            'msg',
            'createdAt'
        )