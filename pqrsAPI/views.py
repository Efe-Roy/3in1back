from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)
from .serializers import (PqrsMainSerializer, EntityTypeSerializer, 
                          NameTypeSerializer, AllPqrsSerializer, RestrictedPqrsMaintSerializer,
                          MediumResTypeSerializer, InnerFormPqrsMaintSerializer
                          )
from .models import PqrsMain, EntityType, NameType, MediumResType, FileResNum
from Auth.models import Agent, Team

from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.authentication import TokenAuthentication

# Create your views here.
class get_all_entityType(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EntityTypeSerializer
    queryset = EntityType.objects.all()

class get_all_nameType(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = NameTypeSerializer
    queryset = NameType.objects.all()

class get_all_mediumRes(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MediumResTypeSerializer
    queryset = MediumResType.objects.all()

class get_all_pqrs2(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AllPqrsSerializer
    queryset = PqrsMain.objects.all()

# class In_Form_pqrs(UpdateAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = InnerFormPqrsMaintSerializer
#     queryset = PqrsMain.objects.all()

class In_Form_pqrs(APIView):
    def get_object(self, pk):
        try:
            return PqrsMain.objects.get(id=pk)
        except PqrsMain.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        PqrsById = self.get_object(pk)

        serializer = InnerFormPqrsMaintSerializer(PqrsById, data=request.data)
        if serializer.is_valid():
            print("erase", request.data["file_res"])

            get_file = FileResNum.objects.all()

            if get_file.exists():
                last_file = FileResNum.objects.all().order_by('-id').first()
                upId = last_file.id

                newFile_res_num = FileResNum.objects.get(id=upId)
                newFile_res_num.name = request.data["file_res"]
                newFile_res_num.save()

            else:
                print("getIndex is None")
                file_num = 1
                d = "RR-" + "%04d" % (file_num,) + "-2023"
                FileResNum.objects.create(name=d)
                print(d)

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)



class get_post_pqrs(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        queryset = PqrsMain.objects.all()
        serializerPqrs = AllPqrsSerializer(queryset, many=True)
        # serializerPqrs = PqrsMainSerializer(queryset, many=True)
        return Response( serializerPqrs.data)

    def post(self, request, format=None):
        serializer = RestrictedPqrsMaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)


class get_details_pqrs(APIView):
    def get_object(self, pk):
        try:
            return PqrsMain.objects.get(id=pk)
        except PqrsMain.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        PqrsById = self.get_object(pk)
        
        serializer = AllPqrsSerializer(PqrsById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        PqrsById = self.get_object(pk)
        serializer = PqrsMainSerializer(PqrsById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        PqrsById = self.get_object(pk)
        PqrsById.delete()
        return Response(status= HTTP_204_NO_CONTENT)


class CurrentFileNumView(APIView):
    def get(self, request, format=None):
        get_file = PqrsMain.objects.all()


        if get_file.exists():
            print("Has Data")
            last_file = PqrsMain.objects.all().order_by('-id')[0]
            # file_num = int(last_file.file_num) + 1

            # string = "0001-2023"
            string = last_file.file_num
            parts = string.split("-")
            number = parts[0]
            print(number)
            file_num = int(number) + 1
            d = "%04d" % ( file_num, ) + "-2023"

            # d = "%04d" % ( file_num, )
            print(d)
        else:
            print("Empty")
            file_num = 1
            d = "%04d" % ( file_num, ) + "-2023"

            # d = "%04d" % ( file_num, )
            print(d)

        return Response(d)

class FileResNumView(APIView):
    def get(self, request, format=None):

        get_file = FileResNum.objects.all()

        if get_file.exists():
            print("Has Data")
            last_file = FileResNum.objects.all().order_by('-id').first()
            getIndex = last_file.name
            # print("xcx", getIndex)
            
            # do more
            if getIndex:
                part = getIndex.split('-')
                desired_value = part[1]
                file_num = int(desired_value) + 1
                d = "RR-" + "%04d" % (file_num,) + "-2023"
                # print(d)
                print("new File Num", d)
            else:
                print("getIndex is None")
                file_num = 1
                d = "RR-" + "%04d" % (file_num,) + "-2023"

        else:
            print("getIndex is None")
            file_num = 1
            d = "RR-" + "%04d" % (file_num,) + "-2023"
            # FileResNum.objects.create(name=d)
            print(d)
            
        

        return Response(d)

