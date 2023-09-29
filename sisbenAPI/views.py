from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView, ListCreateAPIView
)
from .serializers import SisbenMainSerializer
from .models import SisbenMain

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
