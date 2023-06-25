from rest_framework import serializers
from .models import ContratacionMain, processType, acroymsType, typologyType, resSecType, StateType


class AllContratacionMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratacionMain
        fields = '__all__'

class ProcessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = processType
        fields = '__all__'

class AcroymsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = acroymsType
        fields = '__all__'

class TypologyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = typologyType
        fields = '__all__'

class ResSecTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = resSecType
        fields = '__all__'

class StateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateType
        fields = '__all__'


class ContratacionMainSerializer(serializers.ModelSerializer):
    process = serializers.SerializerMethodField()
    acroyms_of_contract = serializers.SerializerMethodField()
    typology = serializers.SerializerMethodField()
    responsible_secretary = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    class Meta:
        model = ContratacionMain
        fields = (
          'id', 'process', 'acroyms_of_contract', 'typology', 'contact_no',
          'contractor', 'contractor_identification', 'verification_digit', 
          'birthday_date', 'blood_type', 'sex', 'object', 'worth', 'duration',
          'contract_date', 'start_date', 'finish_date', 'advance', 'report_secop_begins',
          'secop_contract_report', 'report_honest_antioquia', 'report_institute_web',
          'sia_observe_report', 'act_liquidation', 'settlement_report', 'close_record_and_report_date',
          'addition', 'value_added', 'extra_time', 'bpin_project_code', 'value_affected_bpin_proj_cdp',
          'budget_items', 'article_name', 'item_value', 'state', 'responsible_secretary',
          'name_supervisor_or_controller', 'observations', 'contract_value_plus',
          'real_executed_value_according_to_settlement', 'file_status'
        )

    def get_process(self, obj):
        return ProcessTypeSerializer(obj.process).data
    
    def get_acroyms_of_contract(self, obj):
        return AcroymsTypeSerializer(obj.acroyms_of_contract).data
    
    def get_typology(self, obj):
        return TypologyTypeSerializer(obj.typology).data
    
    def get_responsible_secretary(self, obj):
        return ResSecTypeSerializer(obj.responsible_secretary).data
    
    def get_state(self, obj):
        return StateTypeSerializer(obj.state).data
