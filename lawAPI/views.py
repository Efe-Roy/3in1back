from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from .serializers import PreviousStudySerializer, PreviousStudySerializer2
from .models import PreviousStudyModel
from contratacionAPI.models import resSecType
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count

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
    