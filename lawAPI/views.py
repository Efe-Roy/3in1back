from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from .serializers import PreviousStudySerializer, PreviousStudySerializer2
from .models import PreviousStudyModel
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'PageSize'

class PrevStudListView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PreviousStudySerializer2
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = PreviousStudyModel.objects.all().order_by('-createdAt')
        # queryset = PreviousStudyModel.objects.all()

        # Filter based on request parameters
        process_id = self.request.query_params.get('process_id', None)
        if process_id:
            queryset = queryset.filter(process_id=process_id)

        return queryset


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
    