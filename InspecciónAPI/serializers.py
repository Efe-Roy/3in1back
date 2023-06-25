from rest_framework import serializers
from .models import PoliceCompliant, UrbanControl, PoliceSubmissionLGGS, TrafficViolationCompared, TrafficViolationComparedMyColission, ComplaintAndOfficeToAttend, File2Return2dOffice


class PoliceCompliantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceCompliant
        fields = '__all__'

class UrbanControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrbanControl
        fields = '__all__'

class PoliceSubmissionLGGSSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceSubmissionLGGS
        fields = '__all__'

class TrafficViolationComparedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficViolationCompared
        fields = '__all__'

class TrafficViolationComparedMyColissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficViolationComparedMyColission
        fields = '__all__'

class ComplaintAndOfficeToAttendSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintAndOfficeToAttend
        fields = '__all__'

class File2Return2dOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = File2Return2dOffice
        fields = '__all__'
