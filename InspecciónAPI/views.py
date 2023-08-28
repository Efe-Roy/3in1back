from django.shortcuts import render
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.authentication import TokenAuthentication
from .models import PoliceCompliant, UrbanControl, PoliceSubmissionLGGS, TrafficViolationCompared, TrafficViolationComparedMyColission, ComplaintAndOfficeToAttend, File2Return2dOffice
from .serializers import ( 
    PoliceCompliantSerializer, ByIdPoliceCompliantSerializer, PoliceCompliantSerializer2,
    UrbanControlSerializer,ByIdUrbanControlSerializer, UrbanControlSerializer2,
    PoliceSubmissionLGGSSerializer, ByIdPoliceSubmissionLGGSSerializer, PoliceSubmissionLGGSSerializer2,
    TrafficViolationComparedSerializer, ByIdTrafficViolationComparedSerializer, TrafficViolationComparedSerializer2,
    TrafficViolationComparedMyColissionSerializer, ByIdTrafficViolationComparedMyColissionSerializer,TrafficViolationComparedMyColissionSerializer2,
    ComplaintAndOfficeToAttendSerializer, ByIdComplaintAndOfficeToAttendSerializer, ComplaintAndOfficeToAttendSerializer2,
    File2Return2dOfficeSerializer, ByIdFile2Return2dOfficeSerializer, File2Return2dOfficeSerializer2
)
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView, GenericAPIView,
    ListCreateAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from Auth.models import Agent
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
# PoliceSubmissionLGGSSerializer 
class PoliceCompliantView(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        queryset = PoliceCompliant.objects.all()
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
            email_body = f'Hola {agent.user.username}, \n Se te ha asignado un nuevo fichero en QUERELLA DE POLICIA'
            data = {'email_body': email_body, 'to_email': agent.user.email,
                    'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

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
        queryset = UrbanControl.objects.all().order_by('-id')
        serializer = UrbanControlSerializer2(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = UrbanControlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
           
            agent_id = request.data['assign_team']
            agent = Agent.objects.get(id=agent_id)
            print("email", agent.user.email)

            # Send activation email
            email_body = f'Hola {agent.user.username}, \n Se te ha asignado un nuevo fichero en CONTROL URBAN'
            data = {'email_body': email_body, 'to_email': agent.user.email,
                    'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            

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
        queryset = PoliceSubmissionLGGS.objects.all().order_by('-id')
        serializer = PoliceSubmissionLGGSSerializer2(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = PoliceSubmissionLGGSSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            agent_id = request.data['assign_team']
            agent = Agent.objects.get(id=agent_id)
            print("email", agent.user.email)

            # Send activation email
            email_body = f'Hola {agent.user.username}, \n Se te ha asignado un nuevo fichero en COMPARENDOS POLICIVOS RADICADOS EN LA SECRETARIA GENERAL Y DE GOIERNO'
            data = {'email_body': email_body, 'to_email': agent.user.email,
                    'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            
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
        queryset = TrafficViolationCompared.objects.all().order_by('-id')
        serializer = TrafficViolationComparedSerializer2(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = TrafficViolationComparedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            agent_id = request.data['assign_team']
            agent = Agent.objects.get(id=agent_id)
            print("email", agent.user.email)

            # Send activation email
            email_body = f'Hola {agent.user.username}, \n Se te ha asignado un nuevo fichero en CONTRAVENCIONES DE TRANSITO POR COMPARENDO'
            data = {'email_body': email_body, 'to_email': agent.user.email,
                    'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            
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
        queryset = TrafficViolationComparedMyColission.objects.all().order_by('-id')
        serializer = TrafficViolationComparedMyColissionSerializer2(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = TrafficViolationComparedMyColissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            agent_id = request.data['assign_team']
            agent = Agent.objects.get(id=agent_id)
            print("email", agent.user.email)

            # Send activation email
            email_body = f'Hola {agent.user.username}, \n Se te ha asignado un nuevo fichero en CONTRAVENCIONES DE TRANSITO POR COLISION'
            data = {'email_body': email_body, 'to_email': agent.user.email,
                    'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            
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
        queryset = ComplaintAndOfficeToAttend.objects.all().order_by('-id')
        serializer = ComplaintAndOfficeToAttendSerializer2(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = ComplaintAndOfficeToAttendSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            agent_id = request.data['assign_team']
            agent = Agent.objects.get(id=agent_id)
            print("email", agent.user.email)

            # Send activation email
            email_body = f'Hola {agent.user.username}, \n Se te ha asignado un nuevo fichero en QUEJAS Y OFICIOS POR ATENDER'
            data = {'email_body': email_body, 'to_email': agent.user.email,
                    'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            
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
        queryset = File2Return2dOffice.objects.all().order_by('-id')
        serializer = File2Return2dOfficeSerializer2(queryset, many=True)
        return Response( serializer.data)

    def post(self, request, format=None):
        serializer = File2Return2dOfficeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            agent_id = request.data['assign_team']
            agent = Agent.objects.get(id=agent_id)
            print("email", agent.user.email)

            # Send activation email
            email_body = f'Hola {agent.user.username}, \n Se te ha asignado un nuevo fichero en EXPEDIENTE PARA DEVOLVER AL DESPACHO DE PRIMERA INSTANCIA'
            data = {'email_body': email_body, 'to_email': agent.user.email,
                    'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            
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
