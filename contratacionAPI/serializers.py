from rest_framework import serializers
from .models import ( 
    ContratacionMain, processType, acroymsType, 
    typologyType, resSecType, StateType, 

    ValueAdded, BpinProjectCode, ValueAffectedBpinProjCDP,
    BudgetItems, ArticleName, ItemValue
)


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




class ValueAddedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValueAdded
        fields = ('name',)

class BpinProjectCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BpinProjectCode
        fields = ('name',)

class ValueAffectedBpinProjCDPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValueAffectedBpinProjCDP
        fields = ('name',)

class BudgetItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetItems
        fields = ('name',)

class ArticleNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleName
        fields = ('name',)

class ItemValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemValue
        fields = ('name',)


class AllContratacionMainSerializer(serializers.ModelSerializer):
    value_added = ValueAddedSerializer(many=True)
    bpin_project_code = BpinProjectCodeSerializer(many=True)
    value_affected_bpin_proj_cdp = ValueAffectedBpinProjCDPSerializer(many=True)
    budget_items = BudgetItemsSerializer(many=True)
    article_name = ArticleNameSerializer(many=True)
    item_value = ItemValueSerializer(many=True)

    class Meta:
        model = ContratacionMain
        fields = (
          'process', 'process_num', 'acroyms_of_contract', 'typology', 'contact_no',
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

    def create(self, validated_data):
        value_added_datas = validated_data.pop('value_added')
        bpin_project_code_datas = validated_data.pop('bpin_project_code')
        value_affected_bpin_proj_cdp_datas = validated_data.pop('value_affected_bpin_proj_cdp')
        budget_items_datas = validated_data.pop('budget_items')
        article_name_datas = validated_data.pop('article_name')
        item_value_datas = validated_data.pop('item_value')

        contratacion = ContratacionMain.objects.create(**validated_data)

        for value_added_data in value_added_datas:
            resData = ValueAdded.objects.create(**value_added_data)
            contratacion.value_added.add(resData)

        for bpin_project_code_data in bpin_project_code_datas:
            resData = BpinProjectCode.objects.create(**bpin_project_code_data)
            contratacion.bpin_project_code.add(resData)

        for value_affected_bpin_proj_cdp_data in value_affected_bpin_proj_cdp_datas:
            resData = ValueAffectedBpinProjCDP.objects.create(**value_affected_bpin_proj_cdp_data)
            contratacion.value_affected_bpin_proj_cdp.add(resData)

        for budget_items_data in budget_items_datas:
            resData = BudgetItems.objects.create(**budget_items_data)
            contratacion.budget_items.add(resData)

        for article_name_data in article_name_datas:
            resData = ArticleName.objects.create(**article_name_data)
            contratacion.article_name.add(resData)

        for item_value_data in item_value_datas:
            resData = ItemValue.objects.create(**item_value_data)
            contratacion.item_value.add(resData)
            
        return contratacion



class ContratacionMainSerializer(serializers.ModelSerializer):
    process = serializers.SerializerMethodField()
    acroyms_of_contract = serializers.SerializerMethodField()
    typology = serializers.SerializerMethodField()
    responsible_secretary = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    value_added = ValueAddedSerializer(many=True)
    bpin_project_code = BpinProjectCodeSerializer(many=True)
    value_affected_bpin_proj_cdp = ValueAffectedBpinProjCDPSerializer(many=True)
    budget_items = BudgetItemsSerializer(many=True)
    article_name = ArticleNameSerializer(many=True)
    item_value = ItemValueSerializer(many=True)
    
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
    