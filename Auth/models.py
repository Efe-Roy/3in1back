from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from contratacionAPI.models import resSecType


def upload_to(instance, filename):
    return 'profile/{filename}'.format(filename=filename)

def uploadSignature_to(instance, filename):
    return 'signature/{filename}'.format(filename=filename)

class User(AbstractUser):
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    
    image = models.ImageField(_("Image"), upload_to=upload_to, null=True, blank=True)
    is_organisor = models.BooleanField(default=True)
    phone_num = models.CharField(max_length=300, null=True, blank=True)
    position = models.CharField(max_length=300, null=True, blank=True)
    responsible_secretary = models.ForeignKey(resSecType, null=True, blank=True, on_delete=models.SET_NULL)

    signature = models.ImageField(_("Signature"), upload_to=uploadSignature_to, null=True, blank=True)
    approve_signature = models.BooleanField(default=False)

    is_team = models.BooleanField(default=False)
    is_pqrs = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_hiring = models.BooleanField(default=False)
    is_hiring_org = models.BooleanField(default=False)
    is_sisben = models.BooleanField(default=False)
    is_consult = models.BooleanField(default=False)
    is_ticket_admin = models.BooleanField(default=False)
    is_ticket_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f'Profile for user {self.user.username}'
    

class TicketUserAgent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Organisation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Team(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    

class ActivityTracker(models.Model):
    UPDATED = 'update'
    CREATE = 'create'
    DELETE = 'delete'
    EMPTY = 'empty'

    ACTION_CHOICES = (
        (UPDATED, 'update'),
        (CREATE, 'create'),
        (DELETE, 'delete'),
        (EMPTY, 'empty'),
    )
    
    PQRS = 'pqrs'
    INSPECCIÓN = 'inspect'
    CONTRATACIÓN = 'hiring'
    SISBEN = 'sisben'
    EMPTY = 'empty'

    SECTOR_CHOICES = (
        (PQRS, 'pqrs'),
        (INSPECCIÓN, 'inspect'),
        (CONTRATACIÓN, 'hiring'),
        (SISBEN, 'sisben'),
        (EMPTY, 'empty'),
    )

    msg = models.CharField(max_length=500)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, default=EMPTY)
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES, default=EMPTY)
    createdAt = models.DateTimeField(auto_now_add=True)

