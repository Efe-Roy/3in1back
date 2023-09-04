from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.authentication import TokenAuthentication
from .models import ( PoliceCompliant, UrbanControl, PoliceSubmissionLGGS, TrafficViolationCompared, 
                     TrafficViolationComparedMyColission, ComplaintAndOfficeToAttend, File2Return2dOffice,
                     InspNotifify
                     )
from .serializers import ( 
    PoliceCompliantSerializer, ByIdPoliceCompliantSerializer, PoliceCompliantSerializer2,
    UrbanControlSerializer,ByIdUrbanControlSerializer, UrbanControlSerializer2,
    PoliceSubmissionLGGSSerializer, ByIdPoliceSubmissionLGGSSerializer, PoliceSubmissionLGGSSerializer2,
    TrafficViolationComparedSerializer, ByIdTrafficViolationComparedSerializer, TrafficViolationComparedSerializer2,
    TrafficViolationComparedMyColissionSerializer, ByIdTrafficViolationComparedMyColissionSerializer,TrafficViolationComparedMyColissionSerializer2,
    ComplaintAndOfficeToAttendSerializer, ByIdComplaintAndOfficeToAttendSerializer, ComplaintAndOfficeToAttendSerializer2,
    File2Return2dOfficeSerializer, ByIdFile2Return2dOfficeSerializer, File2Return2dOfficeSerializer2, InspNotifySerializer
)
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, GenericAPIView,ListCreateAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from Auth.models import Agent
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import os


# Create your views here.
# PoliceSubmissionLGGSSerializer 
class PoliceCompliantView(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        # queryset = PoliceCompliant.objects.all()

        user = self.request.user
        if user.is_organisor:
            queryset = PoliceCompliant.objects.all().order_by('-id')
            # print("User is_organisor", user.id)
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
            email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en QUERELLA DE POLICIA'
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
        # queryset = UrbanControl.objects.all().order_by('-id')

        user = self.request.user
        if user.is_organisor:
            queryset = UrbanControl.objects.all().order_by('-id')
            # print("User is_organisor", user.id)
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
            email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en CONTROL URBAN'
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
        # queryset = PoliceSubmissionLGGS.objects.all().order_by('-id')

        user = self.request.user
        if user.is_organisor:
            queryset = PoliceSubmissionLGGS.objects.all().order_by('-id')
            # print("User is_organisor", user.id)
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
            email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en COMPARENDOS POLICIVOS RADICADOS EN LA SECRETARIA GENERAL Y DE GOIERNO'
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
        # queryset = TrafficViolationCompared.objects.all().order_by('-id')

        user = self.request.user
        if user.is_organisor:
            queryset = TrafficViolationCompared.objects.all().order_by('-id')
            # print("User is_organisor", user.id)
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
            email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en CONTRAVENCIONES DE TRANSITO POR COMPARENDO'
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
        # queryset = TrafficViolationComparedMyColission.objects.all().order_by('-id')

        user = self.request.user
        if user.is_organisor:
            queryset = TrafficViolationComparedMyColission.objects.all().order_by('-id')
            # print("User is_organisor", user.id)
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
            email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en CONTRAVENCIONES DE TRANSITO POR COLISION'
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
        # queryset = ComplaintAndOfficeToAttend.objects.all().order_by('-id')

        user = self.request.user
        if user.is_organisor:
            queryset = ComplaintAndOfficeToAttend.objects.all().order_by('-id')
            # print("User is_organisor", user.id)
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
            email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en QUEJAS Y OFICIOS POR ATENDER'
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
        # queryset = File2Return2dOffice.objects.all().order_by('-id')

        user = self.request.user
        if user.is_organisor:
            queryset = File2Return2dOffice.objects.all().order_by('-id')
            # print("User is_organisor", user.id)
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
            email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en EXPEDIENTE PARA DEVOLVER AL DESPACHO DE PRIMERA INSTANCIA'
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




class InspNotifyView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        # queryset = InspNotifify.objects.all()

        user = self.request.user
        if user.is_organisor:
            queryset = InspNotifify.objects.all().order_by('-id')
            # print("User is_organisor", user.id)
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
        # Get the uploaded PDF files from the request
        pdf1 = request.FILES.get('pdf1')
        pdf2 = request.FILES.get('pdf2')

        if pdf1 and pdf2:
            # Save the PDF files to temporary locations
            pdf1_path = os.path.join(settings.MEDIA_ROOT, 'temp1.pdf')
            pdf2_path = os.path.join(settings.MEDIA_ROOT, 'temp2.pdf')

            with open(pdf1_path, 'wb') as destination:
                for chunk in pdf1.chunks():
                    destination.write(chunk)
            with open(pdf2_path, 'wb') as destination:
                for chunk in pdf2.chunks():
                    destination.write(chunk)

            # Send the PDFs via email
            subject = 'PDF Attachments'
            message = 'Here are the attached PDF files.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['dakaraefe3@gmail.com']

            email = EmailMessage(subject, message, from_email, recipient_list)
            email.attach_file(pdf1_path)
            email.attach_file(pdf2_path)
            email.send()

            # Clean up the temporary files
            os.remove(pdf1_path)
            os.remove(pdf2_path)

            return Response({'message': 'PDFs sent via email.'}, status=status.HTTP_200_OK)

        return Response({'message': 'Both PDFs are required for upload.'}, status=status.HTTP_400_BAD_REQUEST)
    


