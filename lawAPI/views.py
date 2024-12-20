from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from .serializers import PreviousStudySerializer, PreviousStudySerializer2, OperationSerializer
from .models import PreviousStudyModel, OperationModel
from contratacionAPI.models import resSecType
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from django.http import Http404
from rest_framework import status
from datetime import datetime

# Create your views here.
class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'PageSize'

class PrevStudListView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PreviousStudySerializer2
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = PreviousStudyModel.objects.all()

        # Filter based on request parameters
        process_id = self.request.query_params.get('process_id', None)
        if process_id:
            queryset = queryset.filter(process_id=process_id)

        responsible_secretary_id = self.request.query_params.get('responsible_secretary_id', None)
        if responsible_secretary_id:
            queryset = queryset.filter(responsible_secretary_id=responsible_secretary_id)

        return queryset
 
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Get all distinct values from model
        all_types = resSecType.objects.values_list('name', flat=True)

        # Aggregate counts based on field
        aggregated_responsible_secretary = queryset.values('responsible_secretary__name').annotate(count=Count('id'))
        
        # Create a dictionary to store counts for each 
        responsible_secretary_dict = {item['responsible_secretary__name']: item['count'] for item in aggregated_responsible_secretary}
        
        # Create a list of dictionaries with all values and their counts
        responsible_secretary_result = [{"name": responsible_secretary_type, "count": responsible_secretary_dict.get(responsible_secretary_type, 0)} for responsible_secretary_type in all_types]
        
        # Order the queryset by id
        queryset = queryset.order_by('-id')

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = {
                'results': serializer.data,
                'responsible_secretary_result': responsible_secretary_result,
            }
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'results': serializer.data,
            'responsible_secretary_result': responsible_secretary_result,
        }

        return Response(response_data)
    
class get_post_prev_stud(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        queryset = PreviousStudyModel.objects.all()
        serializerPqrs = PreviousStudySerializer(queryset, many=True)
        return Response( serializerPqrs.data)
    
    def post(self, request, format=None):
        serializer = PreviousStudySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    
class OperationListView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = OperationSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = OperationModel.objects.all().order_by("-id")

        # Filter based on request parameters
        corporate_name = self.request.query_params.get('corporate_name', None)
        if corporate_name:
            queryset = queryset.filter(corporate_name__icontains=corporate_name)

        return queryset
 
class OperationView(APIView):
    # authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        queryset = OperationModel.objects.all()
        serializerPqrs = OperationSerializer(queryset, many=True)
        return Response( serializerPqrs.data)
    
    def post(self, request, format=None):
        serializer = OperationSerializer(data=request.data)
        automated_number = self.generate_automated_number() 
        print("hh -- kk", automated_number)

        if serializer.is_valid():
            serializer.validated_data['consecutive_numbering'] = automated_number
            serializer.save()

            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def generate_automated_number(cls):
        year = datetime.now().year
        obj = OperationModel.objects.all()
        if obj.exists():
            last_obj = OperationModel.objects.all().order_by('-id').first()
            getIndex = last_obj.consecutive_numbering

            if getIndex:
                part = getIndex.split('-')
                desired_value = part[0]
                file_num = int(desired_value) + 1
                ed = "%03d" % ( file_num, )
                return f'{ed}-{year}'
            else:
                return f'001-{year}'
        else:
            return f'001-{year}'
        
class OperationDetailView(APIView):
    def get_object(self, pk):
        try:
            return OperationModel.objects.get(consecutive_numbering=pk)
        except OperationModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = OperationSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        user = self.request.user
        # request.data['authorize_user'] = user.id

        serializer = OperationSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['authorize_user'] = user
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    