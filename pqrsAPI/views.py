from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView, ListCreateAPIView
)
from .serializers import (PqrsMainSerializer, EntityTypeSerializer, PqrsNotifySerializer,
                          NameTypeSerializer, AllPqrsSerializer,
                          MediumResTypeSerializer, InnerFormPqrsMaintSerializer, StatusTypeSerializer
                          )
from .models import PqrsMain, EntityType, NameType, MediumResType, FileResNum, StatusType, PqrsNotifify, PqrsFileNum
from Auth.models import Agent, Team
from datetime import datetime

from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from Auth.models import Team
from django.core.mail import send_mail
from django.conf import settings

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

class get_all_statuType(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StatusTypeSerializer
    queryset = StatusType.objects.all()

class get_all_pqrs2(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AllPqrsSerializer
    queryset = PqrsMain.objects.all()
    
class In_Form_pqrs(APIView):
    def get_object(self, pk):
        try:
            return PqrsMain.objects.get(id=pk)
        except PqrsMain.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        PqrsById = self.get_object(pk)
        automated_number = self.generate_automated_number()

        serializer = InnerFormPqrsMaintSerializer(PqrsById, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['file_res'] = automated_number
            serializer.save()
            self.save_automated_number(automated_number)
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def generate_automated_number(cls):
        year = datetime.now().year
        get_file = FileResNum.objects.all()

        if get_file.exists():
            last_file = FileResNum.objects.all().order_by('-id').first()
            getIndex = last_file.name
            part = getIndex.split('-')
            desired_value = part[1]
            file_num = int(desired_value) + 1
            ed = "%03d" % ( file_num, )
            d = f'RP-{ed}-{year}'
            return d

        else:
            print("getIndex is None")
            file_num = 1
            ed = "%03d" % ( file_num, )
            d = f'RP-{ed}-{year}'
            return d

    def save_automated_number(cls, numData):
        year = datetime.now().year

        existing_object = FileResNum.objects.all()
        if existing_object.exists():
            last_file = FileResNum.objects.all().order_by('-id')[0]
            last_file.name = numData
            last_file.save()
        else:
            file_num = 1
            ed = "%03d" % ( file_num, )
            d = f'RP-{ed}-{year}'
            FileResNum.objects.create(name=d)

    


class get_post_pqrs(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        queryset = PqrsMain.objects.all()
        serializerPqrs = AllPqrsSerializer(queryset, many=True)
        return Response( serializerPqrs.data)

    def post(self, request, format=None):
        serializer = PqrsMainSerializer(data=request.data)
        automated_number = self.generate_automated_number()
        # print("automated_number", automated_number)
        # print("Data", request.data)

        if serializer.is_valid():
            serializer.validated_data['file_num'] = automated_number
            serializer.save()

            self.save_automated_number(automated_number)
           
            if request.data['responsible_for_the_response']:
                team_id = request.data['responsible_for_the_response']
                team = Team.objects.get(id=team_id)

                # Send activation email
                email_body = f'Hola {team.user.username}, \n Se le ha asignado el número de expediente {request.data["file_num"]}.'
                data = {'email_body': email_body, 'to_email': team.user.email,
                        'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
                send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
        
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
    
    def generate_automated_number(cls):
        get_num_file = PqrsFileNum.objects.all()
        year = datetime.now().year

        if get_num_file.exists():
            last_file = PqrsFileNum.objects.all().order_by('-id')[0]

            string = last_file.name
            # print("string", string)
            # parts = string.split("-")
            # number = parts[0]
            file_num = int(string) + 1
            ed = "%03d" % ( file_num, )
            d = f'{ed}-{year}'
            return d
        else:
            file_num = 1
            ed = "%03d" % ( file_num, )
            d = f'{ed}-{year}'
            return d
        
    def save_automated_number(cls, numData):
        existing_object = PqrsFileNum.objects.all()
        parts = numData.split("-")
        number = parts[0]
        if existing_object.exists():
            last_file = PqrsFileNum.objects.all().order_by('-id')[0]
            last_file.name = number
            last_file.save()
        else:
            pass
        
class CustomPagination(PageNumberPagination):
    page_size_query_param = 'PageSize'
    # max_page_size = 100

class get_pqrs(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = AllPqrsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        # queryset = PqrsMain.objects.all()

        user = self.request.user
        if user.is_organisor:
            queryset = PqrsMain.objects.all().order_by('-id')
            # print("User is_organisor", user.id)
        elif user.is_pqrs:
            queryset = PqrsMain.objects.all().order_by('-id')
            # print("User is_pqrs", user.username)
        elif user.is_consult:
            queryset = PqrsMain.objects.all().order_by('-id')
            # print("User is_consult", user.username)
        elif user.is_team:
            foundObject = Team.objects.get(user_id=user.id)
            team_id = foundObject.id
            # print("User is_team", team_id)
            queryset = PqrsMain.objects.filter(responsible_for_the_response_id=team_id).order_by('-id')
        else:
            print("User Unauthorise")
            queryset = None


        # Filter based on request parameters
        name_id = self.request.query_params.get('name_id', None)
        if name_id:
            queryset = queryset.filter(name_id=name_id)
        
        entity_or_position_id = self.request.query_params.get('entity_or_position_id', None)
        if entity_or_position_id:
            queryset = queryset.filter(entity_or_position_id=entity_or_position_id)
   
        date_of_entry = self.request.query_params.get('date_of_entry', None)
        if date_of_entry:
            queryset = queryset.filter(date_of_entry__icontains=date_of_entry)
   
        file_num = self.request.query_params.get('file_num', None)
        if file_num:
            queryset = queryset.filter(file_num__icontains=file_num)
   
        responsible_user_id = self.request.query_params.get('responsible_user_id', None)
        if responsible_user_id:
            # Filter based on the 'user' field within the 'responsible_for_the_response' Team object
            queryset = queryset.filter(responsible_for_the_response__user_id=responsible_user_id)
        
   
        return queryset

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
        get_num_file = PqrsFileNum.objects.all()
        year = datetime.now().year

        if get_num_file.exists():
            print("Has Data nn")
            last_file = PqrsFileNum.objects.all().order_by('-id')[0]

            string = last_file.name
            parts = string.split("-")
            number = parts[0]
            # num2 = parts[1]
            file_num = int(number) + 1
            ed = "%03d" % ( file_num, )
            d = f'{ed}-{year}'

            # print(num2)
        else:
            print("Empty")
            file_num = 1
            ed = "%03d" % ( file_num, )
            d = f'{ed}-{year}'
            # print(d)

        return Response(d)

class FileResNumView(APIView):
    def get(self, request, format=None):
        year = datetime.now().year

        get_file = FileResNum.objects.all()

        if get_file.exists():
            # print("Has Data")
            last_file = FileResNum.objects.all().order_by('-id').first()
            getIndex = last_file.name
            # print("xcx", getIndex)
            
            # do more
            if getIndex:
                part = getIndex.split('-')
                desired_value = part[1]
                file_num = int(desired_value) + 1
                ed = "%03d" % ( file_num, )
                d = f'RP-{ed}-{year}'
                # print("new File Num", d)
            else:
                # print("getIndex is None")
                file_num = 1
                ed = "%03d" % ( file_num, )
                d = f'RR-{ed}-{year}'

        else:
            # print("getIndex is None")
            file_num = 1
            # d = "RR-" + "%04d" % (file_num,) + "-" + {year}
            file_num = 1
            ed = "%03d" % ( file_num, )
            d = f'RP-{ed}-{year}'
            # print(d)
        
        return Response(d)

class PqrsNotifyView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PqrsNotifySerializer
    queryset = PqrsNotifify.objects.all()