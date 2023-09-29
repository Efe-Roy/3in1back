from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ( ListCreateAPIView )
from .serializers import SisbenMainSerializer
from .models import SisbenMain
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
   
        return queryset


@api_view(['POST'])
def delete_data(request):
    try:
        # Delete all records from the table
        SisbenMain.objects.all().delete()
        return Response({'message': 'All data deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
