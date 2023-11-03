from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView, ListCreateAPIView
)
from .serializers import (PqrsMainSerializer, EntityTypeSerializer, PqrsNotifySerializer,
                          NameTypeSerializer, AllPqrsSerializer, RestrictedPqrsMaintSerializer,
                          MediumResTypeSerializer, InnerFormPqrsMaintSerializer, StatusTypeSerializer
                          )
from .models import PqrsMain, EntityType, NameType, MediumResType, FileResNum, StatusType, PqrsNotifify
from Auth.models import Agent, Team

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
            # print("status", PqrsById.status_of_the_response.id)

            get_file = FileResNum.objects.all()

            if get_file.exists():
                last_file = FileResNum.objects.all().order_by('-id').first()
                upId = last_file.id
                getIndex = last_file.name
                part = getIndex.split('-')
                desired_value = part[1]
                file_num = int(desired_value) + 1
                d = "RR-" + "%04d" % (file_num,) + "-2023"
                # print("Men Like Roy", d)

                newFile_res_num = FileResNum.objects.get(id=upId)
                # newFile_res_num.name = request.data["file_res"]
                newFile_res_num.name = d
                newFile_res_num.save()

            else:
                print("getIndex is None")
                file_num = 1
                d = "RR-" + "%04d" % (file_num,) + "-2023"
                FileResNum.objects.create(name=d)
                # print(d)

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)



class get_post_pqrs(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        queryset = PqrsMain.objects.all()
        serializerPqrs = AllPqrsSerializer(queryset, many=True)
        return Response( serializerPqrs.data)

    def post(self, request, format=None):
        serializer = RestrictedPqrsMaintSerializer(data=request.data)
        # print("zzzxxxcccvvv", request.data["responsible_for_the_response"])

        if serializer.is_valid():
            serializer.save()
           
            team_id = request.data['responsible_for_the_response']
            team = Team.objects.get(id=team_id)
            print("email", team.user.email)

            # Send activation email
            email_body = f'Hola {team.user.username}, \n Se le ha asignado el número de expediente {request.data["file_num"]}.'
            data = {'email_body': email_body, 'to_email': team.user.email,
                    'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

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
            queryset = PqrsMain.objects.all()
            # print("User is_organisor", user.id)
        elif user.is_pqrs:
            queryset = PqrsMain.objects.all()
            # print("User is_pqrs", user.username)
        elif user.is_consult:
            queryset = PqrsMain.objects.all()
            # print("User is_consult", user.username)
        elif user.is_team:
            foundObject = Team.objects.get(user_id=user.id)
            team_id = foundObject.id
            # print("User is_team", team_id)
            queryset = PqrsMain.objects.filter(responsible_for_the_response_id=team_id)
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

    

class PqrsNotifyView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PqrsNotifySerializer
    queryset = PqrsNotifify.objects.all()