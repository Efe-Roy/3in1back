from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ( ListCreateAPIView, ListAPIView )
from .serializers import SisbenMainSerializer, LocationTypeSerializer, SisbenMainSerializer2
from .models import SisbenMain, LocationType
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.views import APIView

# Create your views here.
class CustomPagination(PageNumberPagination):
    page_size_query_param = 'PageSize'
    # max_page_size = 100

class get_sisben(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SisbenMainSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = SisbenMain.objects.all()


        # Filter based on request parameters
        full_name = self.request.query_params.get('full_name', None)
        if full_name:
            queryset = queryset.filter(full_name__icontains=full_name)
   
        citizenship_card = self.request.query_params.get('citizenship_card', None)
        if citizenship_card:
            queryset = queryset.filter(citizenship_card__icontains=citizenship_card)
   
        return queryset


class post_sisben(APIView):
    def post(self, request, format=None):
        serializer = SisbenMainSerializer2(data=request.data)
        if serializer.is_valid():
            serializer.save()
           
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
    

class get_all_location(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LocationTypeSerializer
    queryset = LocationType.objects.all()

@api_view(['POST'])
def delete_data(request):
    try:
        # Delete all records from the table
        SisbenMain.objects.all().delete()
        return Response({'message': 'All data deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
