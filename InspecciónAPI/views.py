from django.shortcuts import render
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.authentication import TokenAuthentication
from .models import PoliceCompliant, UrbanControl, PoliceSubmissionLGGS, TrafficViolationCompared, TrafficViolationComparedMyColission, ComplaintAndOfficeToAttend, File2Return2dOffice
from .serializers import PoliceCompliantSerializer, UrbanControlSerializer, PoliceSubmissionLGGSSerializer, TrafficViolationComparedSerializer, TrafficViolationComparedMyColissionSerializer,ComplaintAndOfficeToAttendSerializer, File2Return2dOfficeSerializer

# Create your views here.
# PoliceSubmissionLGGSSerializer 
class PoliceCompliantView(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        queryset = PoliceCompliant.objects.all()
        serializer = PoliceCompliantSerializer(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = PoliceCompliantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class PoliceCompliantDetailView(APIView):
    def get_object(self, pk):
        try:
            return PoliceCompliant.objects.get(id=pk)
        except PoliceCompliant.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = PoliceCompliantSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = PoliceCompliantSerializer(ById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= HTTP_204_NO_CONTENT)
    
class UrbanControlView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        queryset = UrbanControl.objects.all()
        serializer = UrbanControlSerializer(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = UrbanControlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class UrbanControlDetailView(APIView):
    def get_object(self, pk):
        try:
            return UrbanControl.objects.get(id=pk)
        except UrbanControl.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = UrbanControlSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = UrbanControlSerializer(ById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= HTTP_204_NO_CONTENT)
    
class PoliceSubmissionLGGSView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        queryset = PoliceSubmissionLGGS.objects.all()
        serializer = PoliceSubmissionLGGSSerializer(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = PoliceSubmissionLGGSSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class PoliceSubmissionLGGSDetailView(APIView):
    def get_object(self, pk):
        try:
            return PoliceSubmissionLGGS.objects.get(id=pk)
        except PoliceSubmissionLGGS.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = PoliceSubmissionLGGSSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = PoliceSubmissionLGGSSerializer(ById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= HTTP_204_NO_CONTENT)
        
class TrafficViolationComparedView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        queryset = TrafficViolationCompared.objects.all()
        serializer = TrafficViolationComparedSerializer(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = TrafficViolationComparedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class TrafficViolationComparedDetailView(APIView):
    def get_object(self, pk):
        try:
            return TrafficViolationCompared.objects.get(id=pk)
        except TrafficViolationCompared.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = TrafficViolationComparedSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = TrafficViolationComparedSerializer(ById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= HTTP_204_NO_CONTENT)
    
class TrafficViolationComparedMyColissionView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        queryset = TrafficViolationComparedMyColission.objects.all()
        serializer = TrafficViolationComparedMyColissionSerializer(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = TrafficViolationComparedMyColissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class TrafficViolationComparedMyColissionDetailView(APIView):
    def get_object(self, pk):
        try:
            return TrafficViolationComparedMyColission.objects.get(id=pk)
        except TrafficViolationComparedMyColission.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = TrafficViolationComparedMyColissionSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = TrafficViolationComparedMyColissionSerializer(ById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= HTTP_204_NO_CONTENT)
    
class ComplaintAndOfficeToAttendView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        queryset = ComplaintAndOfficeToAttend.objects.all()
        serializer = ComplaintAndOfficeToAttendSerializer(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = ComplaintAndOfficeToAttendSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class ComplaintAndOfficeToAttendDetailView(APIView):
    def get_object(self, pk):
        try:
            return ComplaintAndOfficeToAttend.objects.get(id=pk)
        except ComplaintAndOfficeToAttend.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = ComplaintAndOfficeToAttendSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = ComplaintAndOfficeToAttendSerializer(ById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= HTTP_204_NO_CONTENT)
    
class File2Return2dOfficeView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        queryset = File2Return2dOffice.objects.all()
        serializer = File2Return2dOfficeSerializer(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = File2Return2dOfficeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class File2Return2dOfficeDetailView(APIView):
    def get_object(self, pk):
        try:
            return File2Return2dOffice.objects.get(id=pk)
        except File2Return2dOffice.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = File2Return2dOfficeSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = File2Return2dOfficeSerializer(ById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= HTTP_204_NO_CONTENT)
    