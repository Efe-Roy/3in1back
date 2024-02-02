from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.authentication import TokenAuthentication
from .models import ( 
    PoliceCompliant, UrbanControl, PoliceSubmissionLGGS, TrafficViolationCompared, 
    TrafficViolationComparedMyColission, ComplaintAndOfficeToAttend, File2Return2dOffice,
    InspNotifify, CarNumber, UploadSignedPDF, FilterSelection
    )
from .serializers import ( 
    PoliceCompliantSerializer, ByIdPoliceCompliantSerializer, PoliceCompliantSerializer2,
    UrbanControlSerializer,ByIdUrbanControlSerializer, UrbanControlSerializer2,
    PoliceSubmissionLGGSSerializer, ByIdPoliceSubmissionLGGSSerializer, PoliceSubmissionLGGSSerializer2,
    TrafficViolationComparedSerializer, ByIdTrafficViolationComparedSerializer, TrafficViolationComparedSerializer2,
    TrafficViolationComparedMyColissionSerializer, ByIdTrafficViolationComparedMyColissionSerializer,TrafficViolationComparedMyColissionSerializer2,
    ComplaintAndOfficeToAttendSerializer, ByIdComplaintAndOfficeToAttendSerializer, ComplaintAndOfficeToAttendSerializer2,
    File2Return2dOfficeSerializer, ByIdFile2Return2dOfficeSerializer, File2Return2dOfficeSerializer2, InspNotifySerializer,
    UploadSignedPDFSerializer, ListUploadSignedPDFSerializer, FilterSelectionSerializer
)
from Auth.serializers import AgentSerializer
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, GenericAPIView, ListCreateAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from Auth.models import Agent, User
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
import os
from xhtml2pdf import pisa
import io
from django.template.loader import get_template
from django.utils import timezone
from django.shortcuts import get_object_or_404
import pytz
from datetime import datetime
from django.core.files.base import ContentFile

# Create your views here.   
class PoliceCompliantView(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        # queryset = PoliceCompliant.objects.all()

        user = self.request.user
        if user.is_organisor or user.is_agent_org or user.is_consult:
            queryset = PoliceCompliant.objects.all().order_by('-id')
        elif user.is_agent:
            foundObject = Agent.objects.get(user_id=user.id)
            agent_id = foundObject.id
            # print("User is_team", agent_id)
            queryset = PoliceCompliant.objects.filter(assign_team_id=agent_id)
        else:
            print("User Unauthorise")
            queryset = None

        serializer = PoliceCompliantSerializer2(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = PoliceCompliantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            agent_id = request.data['assign_team']
            agent = Agent.objects.get(id=agent_id)
            print("email", agent.user.email)

            # Send activation email
            # email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en QUERELLA DE POLICIA'
            # data = {'email_body': email_body, 'to_email': agent.user.email,
            #         'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            # send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
    
    def generate_automated_number(cls):
        get_num_file = PoliceCompliant.objects.all()
        year = datetime.now().year

        if get_num_file.exists():
            last_file = PoliceCompliant.objects.all().order_by('-id')[0]

            string = last_file.filed
            year_part = int(string.split('-')[-1])
            if year_part >= year:
               print("Inpec Year is correct")
            else:
                file_num = 1
                ed = "%04d" % ( file_num, )
                d = f'{ed}-{year}'
                print("Afresh Data", d)
            # print("string", string)
            # parts = string.split("-")
            # number = parts[0]
            file_num = int(string) + 1
            ed = "%04d" % ( file_num, )
            d = f'{ed}-{year}'
            return d
        else:
            file_num = 1
            ed = "%04d" % ( file_num, )
            d = f'{ed}-{year}'
            return d
    
class PoliceCompliantDetailView(APIView):
    def get_object(self, pk):
        try:
            return PoliceCompliant.objects.get(id=pk)
        except PoliceCompliant.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = PoliceCompliantSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = PoliceCompliantSerializer(ById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= HTTP_204_NO_CONTENT)
    
class PoliceCompliantPrivateView(UpdateAPIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated, )
    serializer_class = ByIdPoliceCompliantSerializer
    queryset = PoliceCompliant.objects.all()


class UrbanControlView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        # queryset = UrbanControl.objects.all()
        # queryset = UrbanControl.objects.all().order_by('-id')

        user = self.request.user
        if user.is_organisor or user.is_agent_org or user.is_consult:
            queryset = UrbanControl.objects.all().order_by('-id')
        elif user.is_agent:
            foundObject = Agent.objects.get(user_id=user.id)
            agent_id = foundObject.id
            # print("User is_team", agent_id)
            queryset = UrbanControl.objects.filter(assign_team_id=agent_id)
        else:
            print("User Unauthorise")
            queryset = None

        serializer = UrbanControlSerializer2(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = UrbanControlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
           
            agent_id = request.data['assign_team']
            agent = Agent.objects.get(id=agent_id)
            # print("email", agent.user.email)

            notification_msg = "Se te ha asignado un nuevo fichero en CONTROL URBAN"
            InspNotifify.objects.create(msg=notification_msg, assign_team=agent)

            # Send activation email
            # email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en CONTROL URBAN'
            # data = {'email_body': email_body, 'to_email': agent.user.email,
            #         'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            # send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            

            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class UrbanControlDetailView(APIView):
    def get_object(self, pk):
        try:
            return UrbanControl.objects.get(id=pk)
        except UrbanControl.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = UrbanControlSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = UrbanControlSerializer(ById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= HTTP_204_NO_CONTENT)
    
class UrbanControlPrivateView(UpdateAPIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated, )
    serializer_class = ByIdUrbanControlSerializer
    queryset = UrbanControl.objects.all()
    

class PoliceSubmissionLGGSView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        # queryset = PoliceSubmissionLGGS.objects.all().order_by('-id')

        user = self.request.user
        if user.is_organisor or user.is_agent_org or user.is_consult:
            queryset = PoliceSubmissionLGGS.objects.all().order_by('-id')
        elif user.is_agent:
            foundObject = Agent.objects.get(user_id=user.id)
            agent_id = foundObject.id
            # print("User is_team", agent_id)
            queryset = PoliceSubmissionLGGS.objects.filter(assign_team_id=agent_id)
        else:
            print("User Unauthorise")
            queryset = None

        serializer = PoliceSubmissionLGGSSerializer2(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = PoliceSubmissionLGGSSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            agent_id = request.data['assign_team']
            agent = Agent.objects.get(id=agent_id)
            print("email", agent.user.email)

            notification_msg = "Se te ha asignado un nuevo fichero en COMPARENDOS POLICIVOS RADICADOS EN LA SECRETARIA GENERAL Y DE GOIERNO"
            InspNotifify.objects.create(msg=notification_msg, assign_team=agent)

            # Send activation email
            # email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en COMPARENDOS POLICIVOS RADICADOS EN LA SECRETARIA GENERAL Y DE GOIERNO'
            # data = {'email_body': email_body, 'to_email': agent.user.email,
            #         'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            # send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class PoliceSubmissionLGGSDetailView(APIView):
    def get_object(self, pk):
        try:
            return PoliceSubmissionLGGS.objects.get(id=pk)
        except PoliceSubmissionLGGS.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = PoliceSubmissionLGGSSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = PoliceSubmissionLGGSSerializer(ById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= HTTP_204_NO_CONTENT)
        
class PoliceSubmissionLGGSPrivateView(UpdateAPIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated, )
    serializer_class = ByIdPoliceSubmissionLGGSSerializer
    queryset = PoliceSubmissionLGGS.objects.all()


class TrafficViolationComparedView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        # queryset = TrafficViolationCompared.objects.all().order_by('-id')

        user = self.request.user
        if user.is_organisor or user.is_agent_org or user.is_consult:
            queryset = TrafficViolationCompared.objects.all().order_by('-id')
        elif user.is_agent:
            foundObject = Agent.objects.get(user_id=user.id)
            agent_id = foundObject.id
            # print("User is_team", agent_id)
            queryset = TrafficViolationCompared.objects.filter(assign_team_id=agent_id)
        else:
            print("User Unauthorise")
            queryset = None

        serializer = TrafficViolationComparedSerializer2(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = TrafficViolationComparedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            agent_id = request.data['assign_team']
            agent = Agent.objects.get(id=agent_id)
            # print("email", agent.user.email)

            notification_msg = "Se te ha asignado un nuevo fichero en CONTRAVENCIONES DE TRANSITO POR COMPARENDO"
            InspNotifify.objects.create(msg=notification_msg, assign_team=agent)

            # Send activation email
            # email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en CONTRAVENCIONES DE TRANSITO POR COMPARENDO'
            # data = {'email_body': email_body, 'to_email': agent.user.email,
            #         'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            # send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class TrafficViolationComparedDetailView(APIView):
    def get_object(self, pk):
        try:
            return TrafficViolationCompared.objects.get(id=pk)
        except TrafficViolationCompared.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = TrafficViolationComparedSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = TrafficViolationComparedSerializer(ById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= HTTP_204_NO_CONTENT)
    
class TrafficViolationComparedPrivateView(UpdateAPIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated, )
    serializer_class = ByIdTrafficViolationComparedSerializer
    queryset = TrafficViolationCompared.objects.all()


class TrafficViolationComparedMyColissionView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        # queryset = TrafficViolationComparedMyColission.objects.all().order_by('-id')

        user = self.request.user
        if user.is_organisor or user.is_agent_org or user.is_consult:
            queryset = TrafficViolationComparedMyColission.objects.all().order_by('-id')
        elif user.is_agent:
            foundObject = Agent.objects.get(user_id=user.id)
            agent_id = foundObject.id
            # print("User is_team", agent_id)
            queryset = TrafficViolationComparedMyColission.objects.filter(assign_team_id=agent_id)
        else:
            print("User Unauthorise")
            queryset = None


        serializer = TrafficViolationComparedMyColissionSerializer2(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = TrafficViolationComparedMyColissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            agent_id = request.data['assign_team']
            agent = Agent.objects.get(id=agent_id)
            # print("email", agent.user.email)

            notification_msg = "Se te ha asignado un nuevo fichero en CONTRAVENCIONES DE TRANSITO POR COLISION"
            InspNotifify.objects.create(msg=notification_msg, assign_team=agent)

            # Send activation email
            # email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en CONTRAVENCIONES DE TRANSITO POR COLISION'
            # data = {'email_body': email_body, 'to_email': agent.user.email,
            #         'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            # send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class TrafficViolationComparedMyColissionDetailView(APIView):
    def get_object(self, pk):
        try:
            return TrafficViolationComparedMyColission.objects.get(id=pk)
        except TrafficViolationComparedMyColission.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = TrafficViolationComparedMyColissionSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = TrafficViolationComparedMyColissionSerializer(ById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= HTTP_204_NO_CONTENT)

class TrafficViolationComparedMyColissionPrivateView(UpdateAPIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated, )
    serializer_class = ByIdTrafficViolationComparedMyColissionSerializer
    queryset = TrafficViolationComparedMyColission.objects.all()


class ComplaintAndOfficeToAttendView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        # queryset = ComplaintAndOfficeToAttend.objects.all().order_by('-id')

        user = self.request.user
        if user.is_organisor or user.is_agent_org or user.is_consult:
            queryset = ComplaintAndOfficeToAttend.objects.all().order_by('-id')
        elif user.is_agent:
            foundObject = Agent.objects.get(user_id=user.id)
            agent_id = foundObject.id
            # print("User is_team", agent_id)
            queryset = ComplaintAndOfficeToAttend.objects.filter(assign_team_id=agent_id)
        else:
            print("User Unauthorise")
            queryset = None


        serializer = ComplaintAndOfficeToAttendSerializer2(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = ComplaintAndOfficeToAttendSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            agent_id = request.data['assign_team']
            agent = Agent.objects.get(id=agent_id)
            # print("email", agent.user.email)

            notification_msg = "Se te ha asignado un nuevo fichero en QUEJAS Y OFICIOS POR ATENDER"
            InspNotifify.objects.create(msg=notification_msg, assign_team=agent)

            # Send activation email
            # email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en QUEJAS Y OFICIOS POR ATENDER'
            # data = {'email_body': email_body, 'to_email': agent.user.email,
            #         'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            # send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class ComplaintAndOfficeToAttendDetailView(APIView):
    def get_object(self, pk):
        try:
            return ComplaintAndOfficeToAttend.objects.get(id=pk)
        except ComplaintAndOfficeToAttend.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = ComplaintAndOfficeToAttendSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = ComplaintAndOfficeToAttendSerializer(ById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= HTTP_204_NO_CONTENT)
    
class ComplaintAndOfficeToAttendPrivateView(UpdateAPIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated, )
    serializer_class = ByIdComplaintAndOfficeToAttendSerializer
    queryset = ComplaintAndOfficeToAttend.objects.all()


class File2Return2dOfficeView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        # queryset = File2Return2dOffice.objects.all().order_by('-id')

        user = self.request.user
        if user.is_organisor or user.is_agent_org or user.is_consult:
            queryset = File2Return2dOffice.objects.all().order_by('-id')
        elif user.is_agent:
            foundObject = Agent.objects.get(user_id=user.id)
            agent_id = foundObject.id
            # print("User is_team", agent_id)
            queryset = File2Return2dOffice.objects.filter(assign_team_id=agent_id)
        else:
            print("User Unauthorise")
            queryset = None


        serializer = File2Return2dOfficeSerializer2(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = File2Return2dOfficeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            agent_id = request.data['assign_team']
            agent = Agent.objects.get(id=agent_id)
            # print("email", agent.user.email)

            notification_msg = "Se te ha asignado un nuevo fichero en EXPEDIENTE PARA DEVOLVER AL DESPACHO DE PRIMERA INSTANCIA"
            InspNotifify.objects.create(msg=notification_msg, assign_team=agent)


            # Send activation email
            # email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en EXPEDIENTE PARA DEVOLVER AL DESPACHO DE PRIMERA INSTANCIA'
            # data = {'email_body': email_body, 'to_email': agent.user.email,
            #         'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            # send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class File2Return2dOfficeDetailView(APIView):
    def get_object(self, pk):
        try:
            return File2Return2dOffice.objects.get(id=pk)
        except File2Return2dOffice.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = File2Return2dOfficeSerializer(ById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ById = self.get_object(pk)
        serializer = File2Return2dOfficeSerializer(ById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ById = self.get_object(pk)
        ById.delete()
        return Response(status= HTTP_204_NO_CONTENT)
    
class File2Return2dOfficePrivateView(UpdateAPIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated, )
    serializer_class = ByIdFile2Return2dOfficeSerializer
    queryset = File2Return2dOffice.objects.all()


class InspNotifyView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        # queryset = InspNotifify.objects.all()

        user = self.request.user
        if user.is_organisor or user.is_agent_org or user.is_consult:
            queryset = InspNotifify.objects.all().order_by('-id')
        elif user.is_agent:
            foundObject = Agent.objects.get(user_id=user.id)
            agent_id = foundObject.id
            # print("User is_team", agent_id)
            queryset = InspNotifify.objects.filter(assign_team_id=agent_id)
        else:
            print("User Unauthorise")
            queryset = None

        serializer = InspNotifySerializer(queryset, many=True)
        return Response( serializer.data)
    


class UploadPDFView(APIView):
    def post(self, request):
        # Get the uploaded PDF file from the request
        pdf1 = request.FILES.get('pdf1')
        agentId = request.data['agentId']
        # print("vbg", agentId)
        agent = Agent.objects.get(id=agentId)
 
        if pdf1:
            # Send the PDF via email
            subject = 'PDF Attachment'
            message = 'Here is the attached PDF file.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['dakaraefe3@gmail.com']
            # recipient_list = [agent.user.email]

            email = EmailMessage(subject, message, from_email, recipient_list)
            email.attach(pdf1.name, pdf1.read(), pdf1.content_type)
            # email.attach(pdf2.name, pdf2.read(), pdf2.content_type)
            email.send()


            get_file = CarNumber.objects.all()
            if get_file.exists():
                last_file = CarNumber.objects.all().order_by('-id').first()
                # print(last_file)
                upId = last_file.id
                getIndex = last_file.name
                file_num = int(getIndex) + 1
                d = "%03d" % (file_num) 
                print("Men Like Roy", d)

                newCar_num = CarNumber.objects.get(id=upId)
                newCar_num.name = d
                newCar_num.save()

                UploadSignedPDF.objects.create(car_num=d, assign_team=agent)

            return Response({'message': 'PDF sent via email.'}, status=status.HTTP_200_OK)

        return Response({'message': 'A PDF file is required for upload.'}, status=status.HTTP_400_BAD_REQUEST)
    

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'PageSize'

class InspUserListView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AgentSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        # queryset = Agent.objects.all().order_by('-id')
        if self.request.user.is_organisor or self.request.user.is_agent_org:
            queryset = Agent.objects.all().order_by('-id')
        else:
            queryset = None
        return queryset

class ListUpdateAndEmailPDFView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ListUploadSignedPDFSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = UploadSignedPDF.objects.all().order_by('-id')
        return queryset

class ListSelectedFilteredData(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FilterSelectionSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if self.request.user.is_organisor or self.request.user.is_agent_org:
            queryset = FilterSelection.objects.all().order_by('-id')
        else:
            queryset = FilterSelection.objects.filter(assign_team__user=self.request.user).order_by('-id')
        return queryset


class UltimateView(APIView):
    def get(self, request, pk, format=None):
        carNum = self.fetch_CarNum()

        # Filter and serialize each queryset separately
        queryset1 = UrbanControl.objects.filter(assign_team_id=pk)
        serializer1 = UrbanControlSerializer2(queryset1, many=True)

        queryset2 = PoliceCompliant.objects.filter(assign_team_id=pk)
        serializer2 = PoliceCompliantSerializer2(queryset2, many=True)

        queryset3 = PoliceSubmissionLGGS.objects.filter(assign_team_id=pk)
        serializer3 = PoliceSubmissionLGGSSerializer2(queryset3, many=True)

        queryset4 = TrafficViolationCompared.objects.filter(assign_team_id=pk)
        serializer4 = TrafficViolationComparedSerializer2(queryset4, many=True)

        queryset5 = TrafficViolationComparedMyColission.objects.filter(assign_team_id=pk)
        serializer5 = TrafficViolationComparedMyColissionSerializer2(queryset5, many=True)

        queryset6 = ComplaintAndOfficeToAttend.objects.filter(assign_team_id=pk)
        serializer6 = ComplaintAndOfficeToAttendSerializer2(queryset6, many=True)

        queryset7 = File2Return2dOffice.objects.filter(assign_team_id=pk)
        serializer7 = File2Return2dOfficeSerializer2(queryset7, many=True)

        # Combine the serialized data from all querysets
        serialized_data = {
            'urban_control': serializer1.data,
            'police_compliant': serializer2.data,
            'police_submission_lggs': serializer3.data,
            'traffic_violation_compared': serializer4.data,
            'traffic_violation_compared_my_colission': serializer5.data,
            'complaint_and_office_to_attend': serializer6.data,
            'file_2_return_2d_office': serializer7.data,
            'carnum': carNum
        }

        return Response(serialized_data)
    
    def put(self, request, pk, format=None):
        # Update the complete field to True for objects with status_track=False in each queryset
        creatorId = request.data['creatorId']

        # print("sdsd", creatorId)
        agent = Agent.objects.get(id=pk)
        CreatorIntance = User.objects.get(id=creatorId)

        queryset1 = UrbanControl.objects.filter(assign_team_id=pk, status_track=True)
        queryset1.update(status_track=False)

        queryset2 = PoliceCompliant.objects.filter(assign_team_id=pk, status_track=True)
        queryset2.update(status_track=False)

        queryset3 = PoliceSubmissionLGGS.objects.filter(assign_team_id=pk, status_track=True)
        queryset3.update(status_track=False)

        queryset4 = TrafficViolationCompared.objects.filter(assign_team_id=pk, status_track=True)
        queryset4.update(status_track=False)

        queryset5 = TrafficViolationComparedMyColission.objects.filter(assign_team_id=pk, status_track=True)
        queryset5.update(status_track=False)

        queryset6 = ComplaintAndOfficeToAttend.objects.filter(assign_team_id=pk, status_track=True)
        queryset6.update(status_track=False)

        queryset7 = File2Return2dOffice.objects.filter(assign_team_id=pk, status_track=True)
        queryset7.update(status_track=False)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def fetch_CarNum(self):
        get_num_file = CarNumber.objects.all()
        year = datetime.now().year

        if get_num_file.exists():
            last_file = CarNumber.objects.all().order_by('-id')[0]
            string = last_file.name

            if "-" in string:
                year_part = int(string.split('-')[-1])
                if year_part >= year:
                    numeric_part = int(string.split('-')[-2])
                    plus_1 = numeric_part + 1
                    count_str = str(plus_1).zfill(3)
                    return f'{count_str}-{year}'
                else:
                    file_num = 1
                    ed = "%04d" % ( file_num, )
                    return f'{ed}-{year}'
            else:
                file_num = 1
                ed = "%04d" % ( file_num, )
                return f'{ed}-{year}'
        
    
month_mapping = {
    'January': 'enero',
    'February': 'febrero',
    'March': 'marzo',
    'April': 'abril',
    'May': 'mayo',
    'June': 'junio',
    'July': 'julio',
    'August': 'agosto',
    'September': 'septiembre',
    'October': 'octubre',
    'November': 'noviembre',
    'December': 'diciembre',
}

class FilterSelectCreateView(APIView):
    def post(self, request, *args, **kwargs):
        carNum = self.fetch_CarNum()
        assign_agent_id = request.data.get('assign_agent_id', None)
        agent = Agent.objects.get(id=assign_agent_id)

        urbanControl_ids = request.data.get('urbanControl_IDs', [])
        policeCompliant_ids = request.data.get('policeCompliant_IDs', [])
        policeSubmissionLGGS_ids = request.data.get('policeSubmissionLGGS_IDs', [])
        trafficViolationCompared_ids = request.data.get('trafficViolationCompared_IDs', [])
        trafficViolationComparedMyColission_ids = request.data.get('trafficViolationComparedMyColission_IDs', [])
        complaintAndOfficeToAttend_ids = request.data.get('complaintAndOfficeToAttend_IDs', [])
        file2Return2dOffice_ids = request.data.get('file2Return2dOffice_IDs', [])

        # Save track selected data
        filter_selection = FilterSelection(
            car_num= carNum,
            assign_team= agent,
            creator=request.user, 
            # filename= pdf_filename1,
            # pdf_fn1= ContentFile(result.getvalue(), name=pdf_filename1),
            # filename2= pdf_filename2,
            # pdf_fn2= ContentFile(result.getvalue(), name=pdf_filename2),
            selected_urban_control_ids=','.join(map(str, urbanControl_ids)),
            selected_police_compliant_ids=','.join(map(str, policeCompliant_ids)),
            selected_policeSubmissionLGGS_ids=','.join(map(str, policeSubmissionLGGS_ids)),
            selected_trafficViolationCompared_ids=','.join(map(str, trafficViolationCompared_ids)),
            selected_trafficViolationComparedMyColission_ids=','.join(map(str, trafficViolationComparedMyColission_ids)),
            selected_complaintAndOfficeToAttend_ids=','.join(map(str, complaintAndOfficeToAttend_ids)),
            selected_file2Return2dOffice_ids =','.join(map(str, file2Return2dOffice_ids)),
        )
        filter_selection.save()

        # UPDATE CarNum
        self.update_CarNum()

        return Response({'msg': 'Create Successfully'}, status=status.HTTP_200_OK)
    
    def fetch_CarNum(self):
        get_num_file = CarNumber.objects.all()
        year = datetime.now().year

        if get_num_file.exists():
            last_file = CarNumber.objects.all().order_by('-id')[0]
            string = last_file.name

            if "-" in string:
                year_part = int(string.split('-')[-1])
                if year_part >= year:
                    numeric_part = int(string.split('-')[-2])
                    plus_1 = numeric_part + 1
                    count_str = str(plus_1).zfill(3)
                    return f'{count_str}-{year}'
                else:
                    file_num = 1
                    ed = "%04d" % ( file_num, )
                    return f'{ed}-{year}'
            else:
                file_num = 1
                ed = "%04d" % ( file_num, )
                return f'{ed}-{year}'
        
    def update_CarNum(self):
        get_num_file = CarNumber.objects.all()
        year = datetime.now().year

        if get_num_file.exists():
            last_file = CarNumber.objects.all().order_by('-id')[0]
            string = last_file.name
            upId = last_file.id

            if "-" in string:
                year_part = int(string.split('-')[-1])
                if year_part >= year:
                    numeric_part = int(string.split('-')[-2])
                    plus_1 = numeric_part + 1
                    count_str = str(plus_1).zfill(3)
                    d = f'{count_str}-{year}'
                
                    newCar_num = CarNumber.objects.get(id=upId)
                    newCar_num.name = d
                    newCar_num.save()
                else:
                    file_num = 1
                    ed = "%04d" % ( file_num, )
                    d = f'{ed}-{year}'

                    newCar_num = CarNumber.objects.get(id=upId)
                    newCar_num.name = d
                    newCar_num.save()
            else:
                file_num = 1
                ed = "%04d" % ( file_num, )
                d = f'{ed}-{year}'

                newCar_num = CarNumber.objects.get(id=upId)
                newCar_num.name = d
                newCar_num.save()
        

# original logic
class FilterDataView(APIView):
    def post(self, request, *args, **kwargs):
        carNum = self.fetch_CarNum()
        current_date = timezone.now()
        month_in_spanish = month_mapping[current_date.strftime('%B')]

        assign_agent_id = request.data.get('assign_agent_id', None)
        agent = Agent.objects.get(id=assign_agent_id)
        userOrg = User.objects.get(id=request.user.id)
        # print("assign_agent bbb", agent.id)
        # print("user org xxx", request.user.id)


        urbanControl_ids = request.data.get('urbanControl_IDs', [])
        policeCompliant_ids = request.data.get('policeCompliant_IDs', [])
        policeSubmissionLGGS_ids = request.data.get('policeSubmissionLGGS_IDs', [])
        trafficViolationCompared_ids = request.data.get('trafficViolationCompared_IDs', [])
        trafficViolationComparedMyColission_ids = request.data.get('trafficViolationComparedMyColission_IDs', [])
        complaintAndOfficeToAttend_ids = request.data.get('complaintAndOfficeToAttend_IDs', [])
        file2Return2dOffice_ids = request.data.get('file2Return2dOffice_IDs', [])

        queryset1 = UrbanControl.objects.filter(id__in=urbanControl_ids)
        serializer1 = UrbanControlSerializer2(queryset1, many=True)

        queryset2 = PoliceCompliant.objects.filter(id__in=policeCompliant_ids)
        serializer2 = PoliceCompliantSerializer2(queryset2, many=True)

        queryset3 = PoliceSubmissionLGGS.objects.filter(id__in=policeSubmissionLGGS_ids)
        serializer3 = PoliceSubmissionLGGSSerializer2(queryset3, many=True)

        queryset4 = TrafficViolationCompared.objects.filter(id__in=trafficViolationCompared_ids)
        serializer4 = TrafficViolationComparedSerializer2(queryset4, many=True)

        queryset5 = TrafficViolationComparedMyColission.objects.filter(id__in=trafficViolationComparedMyColission_ids)
        serializer5 = TrafficViolationComparedMyColissionSerializer2(queryset5, many=True)

        queryset6 = ComplaintAndOfficeToAttend.objects.filter(id__in=complaintAndOfficeToAttend_ids)
        serializer6 = ComplaintAndOfficeToAttendSerializer2(queryset6, many=True)

        queryset7 = File2Return2dOffice.objects.filter(id__in=file2Return2dOffice_ids)
        serializer7 = File2Return2dOfficeSerializer2(queryset7, many=True)


        serialized_data = {
            'urban_control': serializer1.data,
            'police_compliant': serializer2.data,
            'police_submission_lggs': serializer3.data,
            'traffic_violation_compared': serializer4.data,
            'traffic_violation_compared_my_colission': serializer5.data,
            'complaint_and_office_to_attend': serializer6.data,
            'file_2_return_2d_office': serializer7.data,
        }

        if queryset1 is None:
            print({'error': 'Data not available yet'})

        # Create an HTML template1
        template = get_template('insp/mail.html')
        # template = get_template('insp/AUTO_DE_REPARTO.html')
        context = {
            'urban_control': queryset1,
            'police_compliant': queryset2,
            'police_submission_lggs': queryset3,
            'traffic_violation_compared': queryset4,
            'traffic_violation_compared_my_colission': queryset5,
            'complaint_and_office_to_attend': queryset6,
            'file_2_return_2d_office': queryset7,
            'carNum': carNum,
            'current_date': current_date,
            'month_in_spanish': month_in_spanish,
            'agent': agent,
            'userOrg': userOrg
        }
        html = template.render(context)

        # Generate the PDF1
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)


        # Create an HTML template2
        template2 = get_template('insp/notification.html')
        context2 = {
            'carNum': carNum,
            'current_date': current_date,
            'month_in_spanish': month_in_spanish,
            'agent': agent,
            'userOrg': userOrg,
        }
        html2 = template2.render(context2)

        # Generate the PDF2
        result2 = io.BytesIO()
        pdf2 = pisa.pisaDocument(io.BytesIO(html2.encode("UTF-8")), result2)


        if not pdf.err and not pdf2.err:
            # Generate a dynamic filename
            pdf_filename1 = f'AUTO_DE_REPARTO_{carNum}.pdf'
            pdf_filename2 = f'NOTIFICACIÓN_{carNum}.pdf'

            # Send the PDF via email
            subject = 'PDF Report'
            message = 'Please find attached your PDF report.'
            from_email = settings.EMAIL_HOST_USER
            # recipient_list = ['dakaraefe3@gmail.com', 'dakaraefe@gmail.com']
            recipient_list = [agent.user.email, userOrg.email]

            email = EmailMessage(subject, message, from_email, recipient_list)
            email.content_subtype = "html"
            email.attach(pdf_filename1, result.getvalue(), 'application/pdf')
            email.attach(pdf_filename2, result2.getvalue(), 'application/pdf')
            email.send()

            # Save track selected data
            filter_selection = FilterSelection(
                car_num= carNum,
                assign_team= agent,
                creator=request.user, 
                filename= pdf_filename1,
                pdf_fn1= ContentFile(result.getvalue(), name=pdf_filename1),
                filename2= pdf_filename2,
                pdf_fn2= ContentFile(result.getvalue(), name=pdf_filename2),
                selected_urban_control_ids=','.join(map(str, urbanControl_ids)),
                selected_police_compliant_ids=','.join(map(str, policeCompliant_ids)),
                selected_policeSubmissionLGGS_ids=','.join(map(str, policeSubmissionLGGS_ids)),
                selected_trafficViolationCompared_ids=','.join(map(str, trafficViolationCompared_ids)),
                selected_trafficViolationComparedMyColission_ids=','.join(map(str, trafficViolationComparedMyColission_ids)),
                selected_complaintAndOfficeToAttend_ids=','.join(map(str, complaintAndOfficeToAttend_ids)),
                selected_file2Return2dOffice_ids =','.join(map(str, file2Return2dOffice_ids)),
            )
            filter_selection.save()

            # UPDATE CarNum
            self.update_CarNum()

            return Response(serialized_data, status=status.HTTP_200_OK)
        return Response(serialized_data, status=status.HTTP_200_OK)
    
    def fetch_CarNum(self):
        get_num_file = CarNumber.objects.all()
        year = datetime.now().year

        if get_num_file.exists():
            last_file = CarNumber.objects.all().order_by('-id')[0]
            string = last_file.name

            if "-" in string:
                year_part = int(string.split('-')[-1])
                if year_part >= year:
                    numeric_part = int(string.split('-')[-2])
                    plus_1 = numeric_part + 1
                    count_str = str(plus_1).zfill(3)
                    return f'{count_str}-{year}'
                else:
                    file_num = 1
                    ed = "%04d" % ( file_num, )
                    return f'{ed}-{year}'
            else:
                file_num = 1
                ed = "%04d" % ( file_num, )
                return f'{ed}-{year}'
        
    def update_CarNum(self):
        get_num_file = CarNumber.objects.all()
        year = datetime.now().year

        if get_num_file.exists():
            last_file = CarNumber.objects.all().order_by('-id')[0]
            string = last_file.name
            upId = last_file.id

            if "-" in string:
                year_part = int(string.split('-')[-1])
                if year_part >= year:
                    numeric_part = int(string.split('-')[-2])
                    plus_1 = numeric_part + 1
                    count_str = str(plus_1).zfill(3)
                    d = f'{count_str}-{year}'
                
                    newCar_num = CarNumber.objects.get(id=upId)
                    newCar_num.name = d
                    newCar_num.save()
                else:
                    file_num = 1
                    ed = "%04d" % ( file_num, )
                    d = f'{ed}-{year}'

                    newCar_num = CarNumber.objects.get(id=upId)
                    newCar_num.name = d
                    newCar_num.save()
            else:
                file_num = 1
                ed = "%04d" % ( file_num, )
                d = f'{ed}-{year}'

                newCar_num = CarNumber.objects.get(id=upId)
                newCar_num.name = d
                newCar_num.save()
        
    
class FilteredDataDetailUpdateView(APIView):
    def get(self, request, selection_id):
        # user = request.user

        try:
            filter_selection = FilterSelection.objects.get(id=selection_id)

            urban_control_ids = filter_selection.selected_urban_control_ids.split(',')
            id_list1 = [int(id_str) for id_str in urban_control_ids if id_str.isdigit()]
            queryset_urban_control = UrbanControl.objects.filter(id__in=id_list1)
            serializer_urban_control = UrbanControlSerializer(queryset_urban_control, many=True)

            police_compliant_ids = filter_selection.selected_police_compliant_ids.split()
            id_list2 = [int(id_str) for id_str in police_compliant_ids if id_str.isdigit()]
            queryset_police_compliant = PoliceCompliant.objects.filter(id__in=id_list2)
            serializer_police_compliant = PoliceCompliantSerializer(queryset_police_compliant, many=True)
            
            policeSubmissionLGGS_ids = filter_selection.selected_policeSubmissionLGGS_ids.split()
            id_list3 = [int(id_str) for id_str in policeSubmissionLGGS_ids if id_str.isdigit()]
            queryset_policeSubmissionLGGS = PoliceSubmissionLGGS.objects.filter(id__in=id_list3)
            serializer_policeSubmissionLGGS = PoliceSubmissionLGGSSerializer2(queryset_policeSubmissionLGGS, many=True)

            trafficViolationCompared_ids = filter_selection.selected_trafficViolationCompared_ids.split(',')
            id_list4 = [int(id_str) for id_str in trafficViolationCompared_ids if id_str.isdigit()]
            queryset_trafficViolationCompared = TrafficViolationCompared.objects.filter(id__in=id_list4)
            serializer_trafficViolationCompared = TrafficViolationComparedSerializer2(queryset_trafficViolationCompared, many=True)

            trafficViolationComparedMyColission_ids = filter_selection.selected_trafficViolationComparedMyColission_ids.split()
            id_list5 = [int(id_str) for id_str in trafficViolationComparedMyColission_ids if id_str.isdigit()]
            queryset_trafficViolationComparedMyColission = TrafficViolationComparedMyColission.objects.filter(id__in=id_list5)
            serializer_trafficViolationComparedMyColission = TrafficViolationComparedMyColissionSerializer2(queryset_trafficViolationComparedMyColission, many=True)
       
            complaintAndOfficeToAttend_ids = filter_selection.selected_complaintAndOfficeToAttend_ids.split()
            id_list6 = [int(id_str) for id_str in complaintAndOfficeToAttend_ids if id_str.isdigit()]
            queryset_complaintAndOfficeToAttend = ComplaintAndOfficeToAttend.objects.filter(id__in=id_list6)
            serializer_complaintAndOfficeToAttend = ComplaintAndOfficeToAttendSerializer2(queryset_complaintAndOfficeToAttend, many=True)

            file2Return2dOffice_ids = filter_selection.selected_file2Return2dOffice_ids.split()
            id_list7 = [int(id_str) for id_str in file2Return2dOffice_ids if id_str.isdigit()]
            queryset_file2Return2dOffice = File2Return2dOffice.objects.filter(id__in=id_list7)
            serializer_file2Return2dOffice = File2Return2dOfficeSerializer2(queryset_file2Return2dOffice, many=True)


            response_data = {
                'car_num': filter_selection.car_num,
                'assign_team': filter_selection.assign_team.user.username,
                'agent_signature': filter_selection.agent_signature,
                'organizer_signature': filter_selection.organizer_signature,
                'urban_control': serializer_urban_control.data,
                'police_compliant': serializer_police_compliant.data,
                'police_submission_lggs': serializer_policeSubmissionLGGS.data, 
                'traffic_violation_compared': serializer_trafficViolationCompared.data, 
                'traffic_violation_compared_my_colission': serializer_trafficViolationComparedMyColission.data, 
                'complaint_and_office_to_attend': serializer_complaintAndOfficeToAttend.data, 
                'file_2_return_2d_office': serializer_file2Return2dOffice.data, 
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except FilterSelection.DoesNotExist:
            return Response({'error': 'Filter selection not found for the user'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, selection_id, format=None):
        try:
            filter_selection = FilterSelection.objects.get(id=selection_id)
            current_date = timezone.now()
            month_in_spanish = month_mapping[current_date.strftime('%B')]
            userOrg = User.objects.get(id=request.user.id)

            urban_control_ids = filter_selection.selected_urban_control_ids.split(',')
            id_list1 = [int(id_str) for id_str in urban_control_ids if id_str.isdigit()]
            queryset_urban_control = UrbanControl.objects.filter(id__in=id_list1)
            # serializer_urban_control = UrbanControlSerializer(queryset_urban_control, many=True)

            police_compliant_ids = filter_selection.selected_police_compliant_ids.split()
            id_list2 = [int(id_str) for id_str in police_compliant_ids if id_str.isdigit()]
            queryset_police_compliant = PoliceCompliant.objects.filter(id__in=id_list2)
            # serializer_police_compliant = PoliceCompliantSerializer(queryset_police_compliant, many=True)
            
            policeSubmissionLGGS_ids = filter_selection.selected_policeSubmissionLGGS_ids.split()
            id_list3 = [int(id_str) for id_str in policeSubmissionLGGS_ids if id_str.isdigit()]
            queryset_policeSubmissionLGGS = PoliceSubmissionLGGS.objects.filter(id__in=id_list3)
            # serializer_policeSubmissionLGGS = PoliceSubmissionLGGSSerializer2(queryset_policeSubmissionLGGS, many=True)

            trafficViolationCompared_ids = filter_selection.selected_trafficViolationCompared_ids.split(',')
            id_list4 = [int(id_str) for id_str in trafficViolationCompared_ids if id_str.isdigit()]
            queryset_trafficViolationCompared = TrafficViolationCompared.objects.filter(id__in=id_list4)
            # serializer_trafficViolationCompared = TrafficViolationComparedSerializer2(queryset_trafficViolationCompared, many=True)

            trafficViolationComparedMyColission_ids = filter_selection.selected_trafficViolationComparedMyColission_ids.split()
            id_list5 = [int(id_str) for id_str in trafficViolationComparedMyColission_ids if id_str.isdigit()]
            queryset_trafficViolationComparedMyColission = TrafficViolationComparedMyColission.objects.filter(id__in=id_list5)
            # serializer_trafficViolationComparedMyColission = TrafficViolationComparedMyColissionSerializer2(queryset_trafficViolationComparedMyColission, many=True)
       
            complaintAndOfficeToAttend_ids = filter_selection.selected_complaintAndOfficeToAttend_ids.split()
            id_list6 = [int(id_str) for id_str in complaintAndOfficeToAttend_ids if id_str.isdigit()]
            queryset_complaintAndOfficeToAttend = ComplaintAndOfficeToAttend.objects.filter(id__in=id_list6)
            # serializer_complaintAndOfficeToAttend = ComplaintAndOfficeToAttendSerializer2(queryset_complaintAndOfficeToAttend, many=True)

            file2Return2dOffice_ids = filter_selection.selected_file2Return2dOffice_ids.split()
            id_list7 = [int(id_str) for id_str in file2Return2dOffice_ids if id_str.isdigit()]
            queryset_file2Return2dOffice = File2Return2dOffice.objects.filter(id__in=id_list7)
            # serializer_file2Return2dOffice = File2Return2dOfficeSerializer2(queryset_file2Return2dOffice, many=True)


            # response_data = {
            #     'agent_signature': filter_selection.agent_signature,
            #     'organizer_signature': filter_selection.organizer_signature,
            #     'urban_control': serializer_urban_control.data,
            #     'police_compliant': serializer_police_compliant.data,
            #     'police_submission_lggs': serializer_policeSubmissionLGGS.data, 
            #     'traffic_violation_compared': serializer_trafficViolationCompared.data, 
            #     'traffic_violation_compared_my_colission': serializer_trafficViolationComparedMyColission.data, 
            #     'complaint_and_office_to_attend': serializer_complaintAndOfficeToAttend.data, 
            #     'file_2_return_2d_office': serializer_file2Return2dOffice.data, 
            # }
            
            # Create an HTML template1
            template = get_template('insp/mail.html')
            context = {
                'urban_control': queryset_urban_control,
                'police_compliant': queryset_police_compliant,
                'police_submission_lggs': queryset_policeSubmissionLGGS,
                'traffic_violation_compared': queryset_trafficViolationCompared,
                'traffic_violation_compared_my_colission': queryset_trafficViolationComparedMyColission,
                'complaint_and_office_to_attend': queryset_complaintAndOfficeToAttend,
                'file_2_return_2d_office': queryset_file2Return2dOffice,
                'carNum': filter_selection.car_num,
                'current_date': current_date,
                'month_in_spanish': month_in_spanish,
                'agent': filter_selection.assign_team,
                'userOrg': userOrg
            }
            html = template.render(context)

            # Generate the PDF1
            result = io.BytesIO()
            pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)


            # Create an HTML template2
            template2 = get_template('insp/notification.html')
            context2 = {
                'carNum': filter_selection.car_num,
                'current_date': current_date,
                'month_in_spanish': month_in_spanish,
                'agent': filter_selection.assign_team,
                'userOrg': userOrg,
            }
            html2 = template2.render(context2)

            # Generate the PDF2
            result2 = io.BytesIO()
            pdf2 = pisa.pisaDocument(io.BytesIO(html2.encode("UTF-8")), result2)


            if not pdf.err and not pdf2.err:
                # Generate a dynamic filename
                pdf_filename1 = f'AUTO_DE_REPARTO_{filter_selection.car_num}.pdf'
                pdf_filename2 = f'NOTIFICACIÓN_{filter_selection.car_num}.pdf'

                # Send the PDF via email
                subject = 'PDF Report'
                message = 'Please find attached your PDF report.'
                from_email = settings.EMAIL_HOST_USER
                # recipient_list = ['dakaraefe3@gmail.com', 'dakaraefe@gmail.com']
                recipient_list = [filter_selection.assign_team.user.email, userOrg.email]

                email = EmailMessage(subject, message, from_email, recipient_list)
                email.content_subtype = "html"
                email.attach(pdf_filename1, result.getvalue(), 'application/pdf')
                email.attach(pdf_filename2, result2.getvalue(), 'application/pdf')
                email.send()

                # Update seleted data
                filter_selection.pdf_fn1 = ContentFile(result.getvalue(), name=pdf_filename1)
                filter_selection.pdf_fn2= ContentFile(result.getvalue(), name=pdf_filename2)
                filter_selection.filename= pdf_filename1
                filter_selection.filename2= pdf_filename2
                filter_selection.save()
                
                return Response({'msg': 'PDF generado y guardado exitosamente'}, status=status.HTTP_200_OK)

        except FilterSelection.DoesNotExist:
            return Response({'error': 'Filter selection not found for the user'}, status=status.HTTP_404_NOT_FOUND)
    
    
class CarNum(APIView):
    def get(self, request):
        get_num_file = CarNumber.objects.all()
        year = datetime.now().year

        if get_num_file.exists():
            last_file = CarNumber.objects.all().order_by('-id')[0]
            string = last_file.name

            if "-" in string:
                year_part = int(string.split('-')[-1])
                if year_part >= year:
                    numeric_part = int(string.split('-')[-2])
                    plus_1 = numeric_part + 1
                    count_str = str(plus_1).zfill(3)
                    return Response(f'{count_str}-{year}')
                else:
                    file_num = 1
                    ed = "%04d" % ( file_num, )
                    return Response(f'{ed}-{year}')
            else:
                file_num = 1
                ed = "%04d" % ( file_num, )
                return Response(f'{ed}-{year}')
        
    
class ToggleSignature(APIView):
    def post(self, request, selection_id):
        selection_instance = get_object_or_404(FilterSelection, id=selection_id)

        # Toggle the value
        user = self.request.user
        if user.is_organisor:
            selection_instance.organizer_signature = not selection_instance.organizer_signature
        elif user.is_agent:
            selection_instance.agent_signature = not selection_instance.agent_signature
        else:
            print("User Unauthorise")

        selection_instance.save()
        
        return Response({
            "success": "Field updated successfully",
            "status_organizer": selection_instance.organizer_signature,
            "status_agent": selection_instance.agent_signature
        })
