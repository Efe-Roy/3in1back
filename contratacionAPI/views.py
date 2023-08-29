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

# from django.http import JsonResponse
import json
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum, F, DecimalField, Count
from django.db.models.functions import Cast
from decimal import Decimal


# def jsonRoy(request):
#     data= list(ContratacionMain.objects.values())
#     return JsonResponse(data, safe=False)

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
        # queryset = ContratacionMain.objects.all()

        user = self.request.user
        # print("qaws", user.is_organisor)
        if user.is_organisor:
            queryset = ContratacionMain.objects.all()
            # print("user detail", user.email)
        elif user.is_hiring:
            # print("None Org", user.responsible_secretary_id)
            queryset = ContratacionMain.objects.filter(responsible_secretary_id=user.responsible_secretary_id)
        else:
            queryset = None


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
    

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Count instances where state.name is "EJECUCION"
        ejecucion_count = queryset.filter(state__name="EJECUCION").count()

        # Count instances where state.name is "EJECUCION"
        terminado_count = queryset.filter(state__name="TERMINADO").count()

        # Count instances of each processType
        process_counts = queryset.values('process__name').annotate(process_count=Count('process'))

        # Count instances of each resSecType
        responsible_secretary_counts = queryset.values('responsible_secretary__name').annotate(responsible_secretary_count=Count('responsible_secretary'))

        # Count instances of each stateType
        state_counts = queryset.values('state__name').annotate(state_count=Count('state'))
       
        # Count instances of each typologyType
        typology_counts = queryset.values('typology__name').annotate(typology_count=Count('typology'))

        # Count instances where sex is "Masculino"
        male_count = queryset.filter(sex="Masculino").count()

        # Count instances where sex is "Femenino"
        female_count = queryset.filter(sex="Femenino").count()

        # Calculate the accumulated value of real_executed_value_according_to_settlement
        accumulated_value = queryset.aggregate(
            total_accumulated_value=Sum(
                Cast('real_executed_value_according_to_settlement', output_field=DecimalField(max_digits=15, decimal_places=2))
            )
        )['total_accumulated_value'] or Decimal('0.00')  # Default to 0.00 if no valid values are found

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = {
                'results': serializer.data,
                'accumulated_value': str(accumulated_value),  # Convert Decimal to string for serialization
                'ejecucion_count': ejecucion_count,
                'terminado_count': terminado_count,
                'process_counts': process_counts,
                'responsible_secretary_counts': responsible_secretary_counts,
                'state_counts': state_counts,
                'typology_counts': typology_counts,
                'male_count': male_count,
                'female_count': female_count

            }
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'results': serializer.data,
            'accumulated_value': str(accumulated_value),  # Convert Decimal to string for serialization
            'ejecucion_count': ejecucion_count,
            'terminado_count': terminado_count,
            'process_counts': process_counts,
            'responsible_secretary_counts': responsible_secretary_counts,
            'state_counts': state_counts,
            'typology_counts': typology_counts,
            'male_count': male_count,
            'female_count': female_count

        }

        return Response(response_data)


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
