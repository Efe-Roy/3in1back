from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)
from .serializers import (
    ContratacionMainSerializer, ProcessTypeSerializer, AcroymsTypeSerializer,
    TypologyTypeSerializer, ResSecTypeSerializer, StateTypeSerializer, AllContratacionMainSerializer
    )
from .models import ContratacionMain, processType, acroymsType, typologyType, resSecType, StateType
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
        


class get_details_contratacion(APIView):
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
        serializer = ContratacionMainSerializer(ContratacionById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        PqrsById = self.get_object(pk)
        PqrsById.delete()
        return Response(status= HTTP_204_NO_CONTENT)
