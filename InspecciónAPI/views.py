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
                     InspNotifify, CarNumber, UploadSignedPDF
                     )
from .serializers import ( 
    PoliceCompliantSerializer, ByIdPoliceCompliantSerializer, PoliceCompliantSerializer2,
    UrbanControlSerializer,ByIdUrbanControlSerializer, UrbanControlSerializer2,
    PoliceSubmissionLGGSSerializer, ByIdPoliceSubmissionLGGSSerializer, PoliceSubmissionLGGSSerializer2,
    TrafficViolationComparedSerializer, ByIdTrafficViolationComparedSerializer, TrafficViolationComparedSerializer2,
    TrafficViolationComparedMyColissionSerializer, ByIdTrafficViolationComparedMyColissionSerializer,TrafficViolationComparedMyColissionSerializer2,
    ComplaintAndOfficeToAttendSerializer, ByIdComplaintAndOfficeToAttendSerializer, ComplaintAndOfficeToAttendSerializer2,
    File2Return2dOfficeSerializer, ByIdFile2Return2dOfficeSerializer, File2Return2dOfficeSerializer2, InspNotifySerializer,
    UploadSignedPDFSerializer, ListUploadSignedPDFSerializer
)
from Auth.serializers import AgentSerializer
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, GenericAPIView,ListCreateAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from Auth.models import Agent, User
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
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
            # email_body = f'Hola {agent.user.first_name} {agent.user.last_name}, \n Se te ha asignado un nuevo fichero en QUERELLA DE POLICIA'
            # data = {'email_body': email_body, 'to_email': agent.user.email,
            #         'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Assigned to you'}
            # send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
            
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
    

class UpdateAndEmailPDFView(APIView):
    def put(self, request, pk):
        try:
            signed_pdf = UploadSignedPDF.objects.get(pk=pk)
        except UploadSignedPDF.DoesNotExist:
            return Response({'message': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UploadSignedPDFSerializer(signed_pdf, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            # instance = serializer.save()

            # Send emails with both PDF attachments
            # self.send_email_with_attachments(instance.pdf_file1, instance.pdf_file2)

            return Response({'message': 'Record updated and emails sent successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def send_email_with_attachments(self, pdf_file1, pdf_file2):
    #     # Send an email with both PDF attachments
    #     subject = 'PDF Attachments'
    #     message = 'Please find attached PDFs.'
    #     from_email = settings.EMAIL_HOST_USER
    #     recipient_list = ['dakaraefe3@gmail.com']

    #     # Attach both PDF files
    #     attachments = [(pdf_file1.name, pdf_file1.read(), 'application/pdf'),
    #                    (pdf_file2.name, pdf_file2.read(), 'application/pdf')]

    #     send_mail(subject, message, from_email, recipient_list, fail_silently=False, attachments=attachments)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'PageSize'

class InspUserListView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AgentSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Agent.objects.all().order_by('-id')
        return queryset

class ListUpdateAndEmailPDFView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ListUploadSignedPDFSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = UploadSignedPDF.objects.all().order_by('-id')
        return queryset

class UltimateView(APIView):
    def get(self, request, pk, format=None):
        # Filter and serialize each queryset separately
        queryset1 = UrbanControl.objects.filter(assign_team_id=pk, status_track=False)
        serializer1 = UrbanControlSerializer2(queryset1, many=True)

        queryset2 = PoliceCompliant.objects.filter(assign_team_id=pk, status_track=False)
        serializer2 = PoliceCompliantSerializer2(queryset2, many=True)

        queryset3 = PoliceSubmissionLGGS.objects.filter(assign_team_id=pk, status_track=False)
        serializer3 = PoliceSubmissionLGGSSerializer2(queryset3, many=True)

        queryset4 = TrafficViolationCompared.objects.filter(assign_team_id=pk, status_track=False)
        serializer4 = TrafficViolationComparedSerializer2(queryset4, many=True)

        queryset5 = TrafficViolationComparedMyColission.objects.filter(assign_team_id=pk, status_track=False)
        serializer5 = TrafficViolationComparedMyColissionSerializer2(queryset5, many=True)

        queryset6 = ComplaintAndOfficeToAttend.objects.filter(assign_team_id=pk, status_track=False)
        serializer6 = ComplaintAndOfficeToAttendSerializer2(queryset6, many=True)

        queryset7 = File2Return2dOffice.objects.filter(assign_team_id=pk, status_track=False)
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
        }

        return Response(serialized_data)
    
    def put(self, request, pk, format=None):
        # Update the complete field to True for objects with status_track=False in each queryset
        creatorId = request.data['creatorId']

        # print("sdsd", creatorId)
        agent = Agent.objects.get(id=pk)
        CreatorIntance = User.objects.get(id=creatorId)

        queryset1 = UrbanControl.objects.filter(assign_team_id=pk, status_track=False)
        queryset1.update(status_track=False)

        queryset2 = PoliceCompliant.objects.filter(assign_team_id=pk, status_track=False)
        queryset2.update(status_track=False)

        queryset3 = PoliceSubmissionLGGS.objects.filter(assign_team_id=pk, status_track=False)
        queryset3.update(status_track=False)

        queryset4 = TrafficViolationCompared.objects.filter(assign_team_id=pk, status_track=False)
        queryset4.update(status_track=False)

        queryset5 = TrafficViolationComparedMyColission.objects.filter(assign_team_id=pk, status_track=False)
        queryset5.update(status_track=False)

        queryset6 = ComplaintAndOfficeToAttend.objects.filter(assign_team_id=pk, status_track=False)
        queryset6.update(status_track=False)

        queryset7 = File2Return2dOffice.objects.filter(assign_team_id=pk, status_track=False)
        queryset7.update(status_track=False)



    
        # get_file = CarNumber.objects.all()
        # if get_file.exists():
        #     last_file = CarNumber.objects.all().order_by('-id').first()
        #     # print(last_file)
        #     upId = last_file.id
        #     getIndex = last_file.name
        #     file_num = int(getIndex) + 1
        #     d = "%03d" % (file_num) 
        #     print("Men Like Roy", d)

        #     newCar_num = CarNumber.objects.get(id=upId)
        #     newCar_num.name = d
        #     newCar_num.save()

        #     UploadSignedPDF.objects.create(car_num=d, assign_team=agent, creator=CreatorIntance)

            
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CarNum(APIView):
    def get(self, request):
        get_file = CarNumber.objects.all()
        if get_file.exists():
            last_file = CarNumber.objects.all().order_by('-id').first()
            # print(last_file)
            upId = last_file.id
            getIndex = last_file.name
            file_num = int(getIndex) + 1
            d = "%03d" % (file_num) 
            print("Men Like Roy", d)

            # newCar_num = CarNumber.objects.get(id=upId)
            # newCar_num.name = d
            # newCar_num.save()

            return Response(d)
        

class ToggleSignature(APIView):
    def post(self, request):
        new_value = request.data.get("approve_signature", False)
        userId = request.data['userId']
        instance = User.objects.get(id=userId)
        
        instance.approve_signature = new_value
        instance.save()
        return Response({
            "success": "Field updated successfully",
            "status": new_value
            })
    