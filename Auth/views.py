from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .serializers import (
    UserSerializer, UserProfileSerializer, SignupSerializer, 
    TeamSerializer, AgentSerializer, OperatorSignUpSerializer
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Team, Agent, UserProfile
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)
from rest_framework.parsers import MultiPartParser, FormParser
from django.dispatch import receiver
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.views import APIView
from django.http import Http404


class SignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # "token": Token.objects.get(user=user).key,
            "message": "account create successfully"
        })

class CreateOperatorView(generics.GenericAPIView):
    serializer_class = OperatorSignUpSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()


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
            
        return Response({
            "user": OperatorSignUpSerializer(user, context=self.get_serializer_context()).data,
            "message": "account create successfully"
        })

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user= serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token":token.key,
            "user_id": user.pk,
            "is_organisor": user.is_organisor,
            "is_team": user.is_team,
            "is_agent": user.is_agent,
            "username": user.username,
            "email": user.email,
        })

class UserProfileUpdate(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        print(request.data)
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
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
        serializer = UserProfileSerializer(UserById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserDetail(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class get_all_team(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TeamSerializer
    queryset = Team.objects.all()