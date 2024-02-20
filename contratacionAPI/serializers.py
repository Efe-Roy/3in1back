from rest_framework import serializers
from .models import ( 
    ContratacionMain, processType, acroymsType, 
    typologyType, resSecType, StateType, LawFirmModel,

    ValueAdded, BpinProjectCode, ValueAffectedBpinProjCDP,
    BudgetItems, ArticleName, ItemValue, Notification, SourceOfResources
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

class SourceOfResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceOfResources
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


class PlanContratacionMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratacionMain
        fields = (
            'acroyms_of_contract',
            'contact_no',
            'process',
            'process_num',
            'responsible_secretary',
            'typology',
        )


class AllContratacionMainSerializer(serializers.ModelSerializer):
    value_added = ValueAddedSerializer(many=True)
    bpin_project_code = BpinProjectCodeSerializer(many=True)
    value_affected_bpin_proj_cdp = ValueAffectedBpinProjCDPSerializer(many=True)
    source_of_resources = SourceOfResourcesSerializer(many=True)
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
          'secop_contract_report', 'report_institute_web',
          'sia_observe_report', 'act_liquidation', 'settlement_report', 'close_record', 'report_date',
          'addition', 'url_1', 'url_2', 'value_added', 'extra_time', 'bpin_project_code', 
          'value_affected_bpin_proj_cdp','source_of_resources', 'budget_items', 'article_name', 'item_value', 'state', 
          'responsible_secretary', 'name_supervisor_or_controller', 'observations', 'contract_value_plus',
          'real_executed_value_according_to_settlement', 'file_status', 'program'
        #   , 'report_honest_antioquia'
        )

    def create(self, validated_data):
        value_added_datas = validated_data.pop('value_added')
        bpin_project_code_datas = validated_data.pop('bpin_project_code')
        value_affected_bpin_proj_cdp_datas = validated_data.pop('value_affected_bpin_proj_cdp')
        source_of_resources_datas = validated_data.pop('source_of_resources')
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

        for source_of_resources_data in source_of_resources_datas:
            resData = SourceOfResources.objects.create(**source_of_resources_data)
            contratacion.source_of_resources.add(resData)

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
    
    def update(self, instance, validated_data):
        # Update the fields of the main object (ContratacionMain)
        instance.process = validated_data.get('process', instance.process)
        instance.process_num = validated_data.get('process_num', instance.process_num)
        instance.acroyms_of_contract = validated_data.get('acroyms_of_contract', instance.acroyms_of_contract)
        instance.typology = validated_data.get('typology', instance.typology)
        instance.contact_no = validated_data.get('contact_no', instance.contact_no)
        instance.contractor = validated_data.get('contractor', instance.contractor)
        instance.contractor_identification = validated_data.get('contractor_identification', instance.contractor_identification)
        instance.verification_digit = validated_data.get('verification_digit', instance.verification_digit)
        instance.birthday_date = validated_data.get('birthday_date', instance.birthday_date)
        instance.blood_type = validated_data.get('blood_type', instance.blood_type)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.object = validated_data.get('object', instance.object)
        instance.worth = validated_data.get('worth', instance.worth)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.contract_date = validated_data.get('contract_date', instance.contract_date)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.finish_date = validated_data.get('finish_date', instance.finish_date)
        instance.advance = validated_data.get('advance', instance.advance)
        instance.program = validated_data.get('program', instance.program)
        instance.report_secop_begins = validated_data.get('report_secop_begins', instance.report_secop_begins)
        instance.secop_contract_report = validated_data.get('secop_contract_report', instance.secop_contract_report)
        # instance.report_honest_antioquia = validated_data.get('report_honest_antioquia', instance.report_honest_antioquia)
        instance.report_institute_web = validated_data.get('report_institute_web', instance.report_institute_web)
        instance.sia_observe_report = validated_data.get('sia_observe_report', instance.sia_observe_report)
        instance.act_liquidation = validated_data.get('act_liquidation', instance.act_liquidation)
        instance.settlement_report = validated_data.get('settlement_report', instance.settlement_report)
        instance.close_record = validated_data.get('close_record', instance.close_record)
        instance.report_date = validated_data.get('report_date', instance.report_date)
        instance.addition = validated_data.get('addition', instance.addition)
        instance.url_1 = validated_data.get('url_1', instance.url_1)
        instance.url_2 = validated_data.get('url_2', instance.url_2)
        instance.extra_time = validated_data.get('extra_time', instance.extra_time)
        instance.state = validated_data.get('state', instance.state)
        instance.responsible_secretary = validated_data.get('responsible_secretary', instance.responsible_secretary)
        instance.name_supervisor_or_controller = validated_data.get('name_supervisor_or_controller', instance.name_supervisor_or_controller)
        instance.observations = validated_data.get('observations', instance.observations)
        instance.contract_value_plus = validated_data.get('contract_value_plus', instance.contract_value_plus)
        instance.real_executed_value_according_to_settlement = validated_data.get('real_executed_value_according_to_settlement', instance.real_executed_value_according_to_settlement)
        instance.file_status = validated_data.get('file_status', instance.file_status)

      

        # Update the value_added field (Many-to-many)
        value_added_data = validated_data.get('value_added', [])
        instance.value_added.clear()  # Remove existing related objects
        for item_data in value_added_data:
            value_added_instance = ValueAdded.objects.create(**item_data)
            instance.value_added.add(value_added_instance)  # Add the newly created related object

        # Update the bpin_project_code field (Many-to-many)
        bpin_project_code_data = validated_data.get('bpin_project_code', [])
        instance.bpin_project_code.clear()  # Remove existing related objects
        for item_data in bpin_project_code_data:
            bpin_project_code_instance = BpinProjectCode.objects.create(**item_data)
            instance.bpin_project_code.add(bpin_project_code_instance)

        # Update the value_affected_bpin_proj_cdp field (Many-to-many)
        value_affected_bpin_proj_cdp_data = validated_data.get('value_affected_bpin_proj_cdp', [])
        instance.value_affected_bpin_proj_cdp.clear()
        for item_data in value_affected_bpin_proj_cdp_data:
            value_affected_bpin_proj_cdp_instance = ValueAffectedBpinProjCDP.objects.create(**item_data)
            instance.value_affected_bpin_proj_cdp.add(value_affected_bpin_proj_cdp_instance)
      
        # Update the source_of_resources field (Many-to-many)
        source_of_resources_data = validated_data.get('source_of_resources', [])
        instance.source_of_resources.clear()
        for item_data in source_of_resources_data:
            source_of_resources_instance = SourceOfResources.objects.create(**item_data)
            instance.source_of_resources.add(source_of_resources_instance)
      
        # Update the budget_items field (Many-to-many)
        budget_items_data = validated_data.get('budget_items', [])
        instance.budget_items.clear()
        for item_data in budget_items_data:
            budget_items_instance = BudgetItems.objects.create(**item_data)
            instance.budget_items.add(budget_items_instance)
      
        # Update the article_name field (Many-to-many)
        article_name_data = validated_data.get('article_name', [])
        instance.article_name.clear()
        for item_data in article_name_data:
            article_name_instance = ArticleName.objects.create(**item_data)
            instance.article_name.add(article_name_instance)
      
        # Update the item_value field (Many-to-many)
        item_value_data = validated_data.get('item_value', [])
        instance.item_value.clear()
        for item_data in item_value_data:
            item_value_instance = ItemValue.objects.create(**item_data)
            instance.item_value.add(item_value_instance)

        instance.save()
        return instance


class ContratacionMainSerializer(serializers.ModelSerializer):
    process = serializers.SerializerMethodField()
    acroyms_of_contract = serializers.SerializerMethodField()
    typology = serializers.SerializerMethodField()
    responsible_secretary = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    value_added = ValueAddedSerializer(many=True)
    bpin_project_code = BpinProjectCodeSerializer(many=True)
    value_affected_bpin_proj_cdp = ValueAffectedBpinProjCDPSerializer(many=True)
    source_of_resources = SourceOfResourcesSerializer(many=True)
    budget_items = BudgetItemsSerializer(many=True)
    article_name = ArticleNameSerializer(many=True)
    item_value = ItemValueSerializer(many=True)
    
    class Meta:
        model = ContratacionMain
        fields = (
          'id', 'is_active', 'process', 'process_num', 'acroyms_of_contract', 'typology', 'contact_no',
          'contractor', 'contractor_identification', 'verification_digit', 
          'birthday_date', 'blood_type', 'sex', 'object', 'worth', 'duration',
          'contract_date', 'start_date', 'finish_date', 'advance', 'report_secop_begins',
          'secop_contract_report', 'report_institute_web',
          'sia_observe_report', 'act_liquidation', 'settlement_report', 'close_record', 'report_date', 'source_of_resources',
          'addition', 'url_1', 'url_2', 'value_added', 'extra_time', 'bpin_project_code', 'value_affected_bpin_proj_cdp',
          'budget_items', 'article_name', 'item_value', 'state', 'responsible_secretary',
          'name_supervisor_or_controller', 'observations', 'contract_value_plus',
          'real_executed_value_according_to_settlement', 'file_status', 'program'
        #   , 'report_honest_antioquia'
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
    

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = (
            'id',
            'msg',
            'createdAt'
        )

class LawFirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawFirmModel
        fields = '__all__'
