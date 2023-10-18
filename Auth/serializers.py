from rest_framework import serializers
from .models import User, UserProfile, Team, Agent
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings
from django.core.mail import send_mail



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'username', 'first_name', 'last_name', 'email', 
                'position', 'image', 'signature', 'approve_signature', 
                'is_organisor', 'is_team', 'is_agent', 'is_pqrs', 
                'is_hiring', 'is_hiring_org', 'is_sisben']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_num', 'position', 'image', 'signature', 'approve_signature']

   
class SignupSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['username','email','password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_organisor= True
        user.is_team= False
        user.is_agent= False
        user.is_pqrs= False
        user.is_hiring= False
        user.save()
        UserProfile.objects.create(user=user)
        return user


class OperatorSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_agent', 
                  'is_team', 'is_pqrs', 'is_hiring', 
                  'responsible_secretary', 'is_hiring_org', 'is_sisben']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self, **kwargs):
        email = self.validated_data['email']
        # Auth_user
        # Check if a user with the provided email already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        user = User(
            username=self.validated_data['username'],
            responsible_secretary=self.validated_data['responsible_secretary'],
            email=email,
            is_agent=self.validated_data['is_agent'],
            is_team=self.validated_data['is_team'],
            is_pqrs=self.validated_data['is_pqrs'],
            is_hiring=self.validated_data['is_hiring'],
            is_hiring_org=self.validated_data['is_hiring_org'],
            is_sisben=self.validated_data['is_sisben'],
            is_organisor=False,
            is_active = False,
        )

        password = self.validated_data['password']
        user.set_password(password)
        # user.is_active = False
        user.save()
        return user


class TeamSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('id', 'user')

    def get_user(self, obj):
        return UserSerializer(obj.user).data

class AgentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = ('id', 'user')

    def get_user(self, obj):
        return UserSerializer(obj.user).data

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            # Send email notification
            subject = 'Notificación de cambio de contraseña'
            message = f'su contraseña ha sido cambiada exitosamente. Contraseña de nueva credencial: {password},   Nombre de usuario: {user.username}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)


            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
    
