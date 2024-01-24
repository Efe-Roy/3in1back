from django.db import models
from Auth.models import User
from contratacionAPI.models import processType, resSecType

# Create your models here.
class PreviousStudyModel(models.Model):
    data_receive_mail = models.DateField()
    process = models.ForeignKey(processType, null=True, blank=True, on_delete=models.SET_NULL)
    responsible_secretary = models.ForeignKey(resSecType, null=True, blank=True, on_delete=models.SET_NULL)
    purpose_of_activities = models.TextField()
    worth = models.IntegerField()
    term = models.IntegerField()
    bpin_code = models.IntegerField()
    lawyer_role = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'is_lawyer': True})
    pdf = models.FileField(null=True, blank=True, upload_to='pdfs/lawyer/')
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.process} - {self.data_receive_mail}'


