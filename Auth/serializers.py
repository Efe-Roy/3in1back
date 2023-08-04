from rest_framework import serializers
from .models import User, UserProfile, Team, Agent


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'username', 'email', 'is_organisor', 'is_team', 'is_agent', 'is_pqrs', 'is_hiring']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'image']


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
        user.save()
        UserProfile.objects.create(user=user)
        return user


# class OperatorSignUpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields=['username','email','password', 'is_agent', 'is_team']
#         extra_kwargs={
#             'password':{'write_only':True}
#         }
    
#     def save(self, **kwargs):
#         user = User(
#             username=self.validated_data['username'],
#             email=self.validated_data['email']
#         )
#         password=self.validated_data['password']

#         user.set_password(password)
#         user.is_agent= self.validated_data['is_agent']
#         user.is_team= self.validated_data['is_team']
#         user.is_organisor = False
#         # user.is_active = False

#         user.save()
#         return user


class OperatorSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_agent', 'is_team', 'is_pqrs', 'is_hiring']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self, **kwargs):
        email = self.validated_data['email']

        # Check if a user with the provided email already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        user = User(
            username=self.validated_data['username'],
            email=email,
            is_agent=self.validated_data['is_agent'],
            is_team=self.validated_data['is_team'],
            is_pqrs=self.validated_data['is_pqrs'],
            is_hiring=self.validated_data['is_hiring'],
            is_organisor=False,
        )

        password = self.validated_data['password']
        user.set_password(password)
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
