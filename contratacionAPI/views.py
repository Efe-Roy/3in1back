from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView, ListCreateAPIView
)
from .serializers import (
    ContratacionMainSerializer, ProcessTypeSerializer, AcroymsTypeSerializer,
    TypologyTypeSerializer, ResSecTypeSerializer, StateTypeSerializer, AllContratacionMainSerializer,
    NotificationSerializer
    )
from .models import ContratacionMain, processType, acroymsType, typologyType, resSecType, StateType, Notification
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.authentication import TokenAuthentication

from django.http import JsonResponse
import json
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum
# Create your views here.

def jsonRoy(request):
    data= list(ContratacionMain.objects.values())
    return JsonResponse(data, safe=False)

class get_all_processType(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProcessTypeSerializer
    queryset = processType.objects.all()

class get_all_acroymsType(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AcroymsTypeSerializer
    queryset = acroymsType.objects.all()

class get_all_typologyType(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TypologyTypeSerializer
    queryset = typologyType.objects.all()

class get_all_resSecType(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResSecTypeSerializer
    queryset = resSecType.objects.all()

class get_all_StateType(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StateTypeSerializer
    queryset = StateType.objects.all()


class get_post_contratacion(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        queryset = ContratacionMain.objects.all()
        serializerPqrs = ContratacionMainSerializer(queryset, many=True)
        return Response( serializerPqrs.data)
    
    def post(self, request, format=None):
        serializer = AllContratacionMainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
        


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'PageSize'
    # max_page_size = 100

class get_contratacion(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = ContratacionMainSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = ContratacionMain.objects.all()

        # Filter based on request parameters
        state_id = self.request.query_params.get('state_id', None)
        if state_id:
            queryset = queryset.filter(state_id=state_id)
        
        process_id = self.request.query_params.get('process_id', None)
        if process_id:
            queryset = queryset.filter(process_id=process_id)

        process_num = self.request.query_params.get('process_num', None)
        if process_num:
            queryset = queryset.filter(process_num__icontains=process_num)

        acroyms_of_contract_id = self.request.query_params.get('acroyms_of_contract_id', None)
        if acroyms_of_contract_id:
            queryset = queryset.filter(acroyms_of_contract_id=acroyms_of_contract_id)
        
        responsible_secretary_id = self.request.query_params.get('responsible_secretary_id', None)
        if responsible_secretary_id:
            queryset = queryset.filter(responsible_secretary_id=responsible_secretary_id)

        contractor_identification = self.request.query_params.get('contractor_identification', None)
        if contractor_identification:
            queryset = queryset.filter(contractor_identification__icontains=contractor_identification)

        contractor = self.request.query_params.get('contractor', None)
        if contractor:
            queryset = queryset.filter(contractor__icontains=contractor)

        contact_no = self.request.query_params.get('contact_no', None)
        if contact_no:
            queryset = queryset.filter(contact_no__icontains=contact_no)
        
        sex = self.request.query_params.get('sex', None)
        if sex:
            queryset = queryset.filter(sex__icontains=sex)

        bpin_project_code_names = self.request.query_params.getlist('bpin_project_code', None)
        if bpin_project_code_names:
            queryset = queryset.filter(bpin_project_code__name__in=bpin_project_code_names)

        typology_id = self.request.query_params.get('typology_id', None)
        if typology_id:
            queryset = queryset.filter(typology_id=typology_id)

        return queryset
    
class get_details_contratacion(APIView):
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, pk):
        try:
            return ContratacionMain.objects.get(id=pk)
        except ContratacionMain.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ContratacionById = self.get_object(pk)
        
        serializer = ContratacionMainSerializer(ContratacionById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ContratacionById = self.get_object(pk)
        serializer = AllContratacionMainSerializer(ContratacionById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        PqrsById = self.get_object(pk)
        PqrsById.delete()
        return Response(status= HTTP_204_NO_CONTENT)


class NotificationView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
