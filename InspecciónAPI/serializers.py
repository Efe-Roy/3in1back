from rest_framework import serializers
from .models import PoliceCompliant, UrbanControl, PoliceSubmissionLGGS, TrafficViolationCompared, TrafficViolationComparedMyColission, ComplaintAndOfficeToAttend, File2Return2dOffice


class PoliceCompliantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceCompliant
        fields = '__all__'
class ByIdPoliceCompliantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceCompliant
        fields = ['comment', 'file_res', 'pdf']


class UrbanControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrbanControl
        fields = '__all__'
class ByIdUrbanControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrbanControl
        fields = ['comment', 'file_res', 'pdf']


class PoliceSubmissionLGGSSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceSubmissionLGGS
        fields = '__all__'
class ByIdPoliceSubmissionLGGSSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceSubmissionLGGS
        fields = ['comment', 'file_res', 'pdf']


class TrafficViolationComparedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficViolationCompared
        fields = '__all__'
class ByIdTrafficViolationComparedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficViolationCompared
        fields = ['comment', 'file_res', 'pdf']


class TrafficViolationComparedMyColissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficViolationComparedMyColission
        fields = '__all__'
class ByIdTrafficViolationComparedMyColissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficViolationComparedMyColission
        fields = ['comment', 'file_res', 'pdf']


class ComplaintAndOfficeToAttendSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintAndOfficeToAttend
        fields = '__all__'
class ByIdComplaintAndOfficeToAttendSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintAndOfficeToAttend
        fields = ['comment', 'file_res', 'pdf']


class File2Return2dOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = File2Return2dOffice
        fields = '__all__'
class ByIdFile2Return2dOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = File2Return2dOffice
        fields = ['comment', 'file_res', 'pdf']
