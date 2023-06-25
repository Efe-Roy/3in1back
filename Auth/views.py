from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .serializers import UserSerializer, SignupSerializer, TeamSerializer, ClientSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Team, Agent

from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)

# from django.contrib.auth import get_user_model
from django.dispatch import receiver


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