from rest_framework import serializers
from .models import ( PoliceCompliant, UrbanControl, PoliceSubmissionLGGS, TrafficViolationCompared, 
                     TrafficViolationComparedMyColission, ComplaintAndOfficeToAttend, File2Return2dOffice,
                     InspNotifify, UploadSignedPDF, FilterSelection
                     )
from Auth.serializers import AgentSerializer, UserSerializer

class PoliceCompliantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceCompliant
        fields = '__all__'
class PoliceCompliantSerializer2(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    assign_team = serializers.SerializerMethodField()
    class Meta:
        model = PoliceCompliant
        fields = ['id', 'creator', 'assign_team', 'filed', 'date_received', 'complainants', 'defendants', 'comment', 'file_res', 'pdf']

    def get_creator(self, obj):
        return UserSerializer(obj.creator).data
    
    def get_assign_team(self, obj):
        return AgentSerializer(obj.assign_team).data
class ByIdPoliceCompliantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceCompliant
        fields = ['comment', 'file_res', 'pdf']


class UrbanControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrbanControl
        fields = '__all__'
class UrbanControlSerializer2(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    assign_team = serializers.SerializerMethodField()
    class Meta:
        model = UrbanControl
        fields = ['id', 'creator', 'assign_team', 'filed', 'date_received', 'Involved_applicant', 'res_report', 'comment', 'file_res', 'pdf']

    def get_creator(self, obj):
        return UserSerializer(obj.creator).data
    
    def get_assign_team(self, obj):
        return AgentSerializer(obj.assign_team).data
class ByIdUrbanControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrbanControl
        fields = ['comment', 'file_res', 'pdf']


class PoliceSubmissionLGGSSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceSubmissionLGGS
        fields = '__all__'
class PoliceSubmissionLGGSSerializer2(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    assign_team = serializers.SerializerMethodField()
    class Meta:
        model = PoliceSubmissionLGGS
        fields = ['id', 'creator', 'assign_team', 'name', 'Id_card', 'appearance_num', 'act_num', 'type_of_identification', 'comment', 'file_res', 'pdf']

    def get_creator(self, obj):
        return UserSerializer(obj.creator).data
    
    def get_assign_team(self, obj):
        return AgentSerializer(obj.assign_team).data
class ByIdPoliceSubmissionLGGSSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceSubmissionLGGS
        fields = ['comment', 'file_res', 'pdf']


class TrafficViolationComparedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficViolationCompared
        fields = '__all__'
class TrafficViolationComparedSerializer2(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    assign_team = serializers.SerializerMethodField()
    class Meta:
        model = TrafficViolationCompared
        fields = ['id', 'creator', 'assign_team', 'date_events', 'date_received', 'compare_number', 'involved', 'id_card', 'violation_code', 'res_procedure', 'comment', 'file_res', 'pdf']

    def get_creator(self, obj):
        return UserSerializer(obj.creator).data
    
    def get_assign_team(self, obj):
        return AgentSerializer(obj.assign_team).data
class ByIdTrafficViolationComparedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficViolationCompared
        fields = ['comment', 'file_res', 'pdf']


class TrafficViolationComparedMyColissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficViolationComparedMyColission
        fields = '__all__'
class TrafficViolationComparedMyColissionSerializer2(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    assign_team = serializers.SerializerMethodField()
    class Meta:
        model = TrafficViolationComparedMyColission
        fields = ['id', 'creator', 'assign_team', 'date_received', 'involved', 'res_procedure', 'comment', 'file_res', 'pdf']

    def get_creator(self, obj):
        return UserSerializer(obj.creator).data
    
    def get_assign_team(self, obj):
        return AgentSerializer(obj.assign_team).data
class ByIdTrafficViolationComparedMyColissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficViolationComparedMyColission
        fields = ['comment', 'file_res', 'pdf']


class ComplaintAndOfficeToAttendSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintAndOfficeToAttend
        fields = '__all__'
class ComplaintAndOfficeToAttendSerializer2(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    assign_team = serializers.SerializerMethodField()
    class Meta:
        model = ComplaintAndOfficeToAttend
        fields = ['id', 'creator', 'assign_team', 'filed', 'date_received', 'affair', 'comment', 'file_res', 'pdf']

    def get_creator(self, obj):
        return UserSerializer(obj.creator).data
    
    def get_assign_team(self, obj):
        return AgentSerializer(obj.assign_team).data
class ByIdComplaintAndOfficeToAttendSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintAndOfficeToAttend
        fields = ['comment', 'file_res', 'pdf']


class File2Return2dOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = File2Return2dOffice
        fields = '__all__'
class File2Return2dOfficeSerializer2(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    assign_team = serializers.SerializerMethodField()
    class Meta:
        model = File2Return2dOffice
        fields = ['id', 'creator', 'assign_team', 'filed', 'guy', 'involved', 'comment', 'file_res', 'pdf']

    def get_creator(self, obj):
        return UserSerializer(obj.creator).data
    
    def get_assign_team(self, obj):
        return AgentSerializer(obj.assign_team).data
class ByIdFile2Return2dOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = File2Return2dOffice
        fields = ['comment', 'file_res', 'pdf']



class InspNotifySerializer(serializers.ModelSerializer):

    class Meta:
        model = InspNotifify
        fields = (
            'id',
            'msg',
            'createdAt',
            'assign_team'
        )

class UploadSignedPDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadSignedPDF
        fields = ['pdf_file1', 'pdf_file2']
        

class ListUploadSignedPDFSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    assign_team = serializers.SerializerMethodField()
    class Meta:
        model = UploadSignedPDF
        fields = ['id', 'car_num', 'assign_team', 'creator', 'pdf_file1', 'pdf_file2', 'createdAt']
        
    def get_creator(self, obj):
        return UserSerializer(obj.creator).data
    
    def get_assign_team(self, obj):
        return AgentSerializer(obj.assign_team).data
    

class FilterSelectionSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    assign_team = serializers.SerializerMethodField()
    class Meta:
        model = FilterSelection
        fields = [
            'id', 'car_num', 'assign_team', 'creator', 
            'filename', 'filename2', 'selected_urban_control_ids', 'selected_police_compliant_ids', 
            'selected_policeSubmissionLGGS_ids', 'selected_trafficViolationCompared_ids', 
            'selected_trafficViolationComparedMyColission_ids', 'selected_complaintAndOfficeToAttend_ids', 
            'selected_file2Return2dOffice_ids', 'timestamp', 'agent_signature', 'organizer_signature'
            ]
    def get_creator(self, obj):
        return UserSerializer(obj.creator).data
    
    def get_assign_team(self, obj):
        return AgentSerializer(obj.assign_team).data
