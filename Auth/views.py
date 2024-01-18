import random
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .serializers import (
    UserSerializer, UserProfileSerializer, SignupSerializer, 
    TeamSerializer, AgentSerializer, OperatorSignUpSerializer,
    ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer,
    ActivityTrackerSerializer
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Team, Agent, ActivityTracker, TicketUserAgent
from rest_framework.views import APIView
from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class SignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
    
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "account create successfully"
        })

class CreateOperatorView(generics.GenericAPIView):
    serializer_class = OperatorSignUpSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        crPass = request.data["password"]
        crName = request.data["username"]
        user = serializer.save()

        # Generate OTP code
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        user.otp_code = otp_code
        user.save()
        
        # Send activation email
        absurl = 'https://procesosadministrativos.com/user/otp'
        email_body = f'Hola, \n Sus credenciales Contraseña: {crPass} y Nombre de usuario: {crName} para iniciar sesión.\n  Para activar su cuenta, use este código OTP: {otp_code}, use el enlace a continuación para restablecer su contraseña  \n' + \
            absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Activa tu cuenta'}
        send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
        
        if user.is_team == True:
            Team.objects.create(
                user=user,
                organisation= self.request.user.userprofile
            )
        if user.is_agent == True:
            Agent.objects.create(
            user=user,
            organisation= self.request.user.userprofile
        )
        if user.is_ticket_agent == True:
            TicketUserAgent.objects.create(user=user)
            
        return Response({
            "user": OperatorSignUpSerializer(user, context=self.get_serializer_context()).data,
            "message": "account create successfully"
        })

class OTPVerificationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        otp_code = request.data.get('otp_code')
        user = User.objects.get(username=username)
        
        if user.otp_code == otp_code:
            user.is_active = True
            user.otp_code = None
            user.save()

            # Send activation email
            subject = 'Activa tu cuenta'
            message = f'Su cuenta ha sido activada, use las credenciales que se le dieron en el correo anterior para iniciar sesión'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            
            send_mail(subject, message, from_email, recipient_list)

            return Response({'message': 'OTP verified and user account activated.'})
        else:
            return Response({'message': 'Invalid OTP code.'}, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user= serializer.validated_data['user']

        if not user.is_active:
            return Response({'message': 'Account is not active.'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token":token.key,
            "user_id": user.pk,
            "is_organisor": user.is_organisor,
            "is_team": user.is_team,
            "is_agent": user.is_agent,
            "is_pqrs": user.is_pqrs,
            "is_hiring": user.is_hiring,
            "is_hiring_org": user.is_hiring_org,
            "is_consult": user.is_consult,
            "is_sisben": user.is_sisben,
            "is_ticket_admin": user.is_ticket_admin,
            "is_ticket_agent": user.is_ticket_agent,
            "username": user.username,
            "email": user.email,
        })

class UserProfileDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        UserById = self.get_object(pk)
        serializer = UserProfileSerializer(UserById)
        return Response( serializer.data)
    
    def put(self, request, pk, format=None):
        UserById = self.get_object(pk)
        image_files = request.FILES.getlist('image[]')
        signature_files = request.FILES.getlist('signature[]')
        
        serializer = UserProfileSerializer(UserById, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            if image_files:
                for image_file in image_files:
                    UserById.image.save(image_file.name, image_file)

            if signature_files:
                for signature_file in signature_files:
                    UserById.signature.save(signature_file.name, signature_file)

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # if image_files:
        #     serializer = UserProfileSerializer(UserById, data=request.data, partial=True)
        #     if serializer.is_valid():
        #         serializer.save()
                
        #         # Save each image file
        #         for image_file in image_files:
        #             UserById.image.save(image_file.name, image_file)
                
        #         return Response(serializer.data)
        #     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        # else:
        #     serializer = UserProfileSerializer(UserById, data=request.data, partial=True)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data)
        #     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'PageSize'

class ActivityTrackerView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActivityTrackerSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = ActivityTracker.objects.all().order_by('-id')

        # Filter based on request parameters
        username = self.request.query_params.get('username', None)
        if username:
            queryset = queryset.filter(user__username__icontains=username)

        first_name = self.request.query_params.get('first_name', None)
        if first_name:
            queryset = queryset.filter(user__first_name__icontains=first_name)

        created_at = self.request.query_params.get('created_at', None)
        if created_at:
            # Assuming createdAt is in the format YYYY-MM-DD, you may need to adjust this based on your actual date format
            queryset = queryset.filter(createdAt__startswith=created_at)
   
        return queryset


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    # queryset = User.objects.filter(is_staff=False).order_by('-date_joined')
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = User.objects.filter(is_staff=False, is_organisor=False).order_by('-date_joined')

        # Filter based on request parameters
        username = self.request.query_params.get('username', None)
        if username:
            queryset = queryset.filter(username__icontains=username)

        is_ticket_agent = self.request.query_params.get('is_ticket_agent', False)
        if is_ticket_agent:
            queryset = queryset.filter(is_ticket_agent=is_ticket_agent)
   
        is_team = self.request.query_params.get('is_team', False)
        if is_team:
            queryset = queryset.filter(is_team=is_team)
   
        is_agent = self.request.query_params.get('is_agent', False)
        if is_agent:
            queryset = queryset.filter(is_agent=is_agent)
   
        is_active = self.request.query_params.get('is_active', False)
        if is_active:
            queryset = queryset.filter(is_active=is_active)
   
        return queryset


class UserDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class get_all_team(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     # permission_classes = (AllowAny,)
#     serializer_class = TeamSerializer
#     # queryset = Team.objects.all()
#     queryset = Team.objects.filter(user__is_active=False)

class ChangePasswordView(APIView):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        # current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        # Check if the current password is correct
        # if not user.check_password(current_password):
        #     return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password and save the user
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password successfully changed.'}, status=status.HTTP_200_OK)
    
class get_all_team(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    # queryset = User.objects.filter(is_staff=False).order_by('-date_joined')
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Team.objects.all()

        # Filter based on request parameters
        is_active = self.request.query_params.get('is_active', False)
        if is_active:
            queryset = queryset.filter(user__is_active=is_active)
   
        return queryset

class get_all_agent(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AgentSerializer
    # queryset = User.objects.filter(is_staff=False).order_by('-date_joined')
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Agent.objects.all()

        # Filter based on request parameters
        is_active = self.request.query_params.get('is_active', False)
        if is_active:
            queryset = queryset.filter(user__is_active=is_active)
   
        return queryset

# class get_all_agent(generics.ListAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = AgentSerializer
#     # queryset = Agent.objects.all()
#     queryset = Agent.objects.filter(user__is_active=False)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            absurl2 = 'https://procesosadministrativos.com/reset-password/'+ uidb64 + '/' + token
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl2
            data = {'email_body': email_body, 'to_email': user.email,
                    'from_email': settings.EMAIL_HOST_USER ,'email_subject': 'Reset your passsword'}
            send_mail(subject=data['email_subject'], message=data['email_body'], from_email=data['from_email'], recipient_list=[data['to_email']])
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'succes': True, 'Message': 'Credential Valid', 'uid64': uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
    

class ActivateDeactivateUser(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        id = request.data.get('id')
        action = request.data.get('action')  # 'activate' or 'deactivate'

        user = self.get_user(id)

        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if action == 'activate':
            user.is_active = True
        elif action == 'deactivate':
            user.is_active = False
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        user.save()

        return Response({'message': f'User {user.username} successfully {action}d'}, status=status.HTTP_200_OK)
    
