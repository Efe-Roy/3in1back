from django.db import models
from Auth.models import UserProfile, Agent, Team, User

# Create your models here.
class PoliceSubmissionLGGS(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_organisor': True})
    assign_team = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=2300, null=True)
    Id_card = models.CharField(max_length=2300, null=True)
    appearance_num = models.CharField(max_length=2300, null=True)
    act_num = models.CharField(max_length=2300, null=True)
    type_of_identification = models.CharField(max_length=2300, null=True)

    comment = models.CharField(max_length=2300, blank=True, null=True)
    file_res = models.CharField(max_length=2300, blank=True, null=True)
    pdf = models.FileField(null=True, blank=True, upload_to='pdfs/PoliceSubmissionLGGS/')

    status_track = models.BooleanField(default=False)


class UrbanControl(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_organisor': True})
    assign_team = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    filed = models.CharField(max_length=2300, null=True)
    date_received = models.DateField(null=True, blank=True)
    Involved_applicant = models.CharField(max_length=2300, null=True)
    res_report = models.CharField(max_length=2300, null=True)

    comment = models.CharField(max_length=2300, blank=True, null=True)
    file_res = models.CharField(max_length=2300, blank=True, null=True)
    pdf = models.FileField(null=True, blank=True, upload_to='pdfs/urbancontrol/')

    status_track = models.BooleanField(default=False)


class PoliceCompliant(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_organisor': True})
    assign_team = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    filed = models.CharField(max_length=2300, null=True)
    date_received = models.DateField(null=True, blank=True)
    complainants = models.CharField(max_length=2300, null=True)
    defendants = models.CharField(max_length=2300, null=True)

    comment = models.CharField(max_length=2300, blank=True, null=True)
    file_res = models.CharField(max_length=2300, blank=True, null=True)
    pdf = models.FileField(null=True, blank=True, upload_to='pdfs/PoliceCompliant/')

    status_track = models.BooleanField(default=False)


class TrafficViolationCompared(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_organisor': True})
    assign_team = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    date_events = models.DateField(null=True, blank=True)
    date_received = models.DateField(null=True, blank=True)
    involved = models.CharField(max_length=2300, null=True)
    id_card = models.CharField(max_length=2300, null=True)
    violation_code = models.CharField(max_length=2300, null=True)
    res_procedure = models.CharField(max_length=2300, null=True)
    compare_number = models.CharField(max_length=2300, null=True) #new....

    comment = models.CharField(max_length=2300, blank=True, null=True)
    file_res = models.CharField(max_length=2300, blank=True, null=True)
    pdf = models.FileField(null=True, blank=True, upload_to='pdfs/TrafficViolationCompared/')

    status_track = models.BooleanField(default=False)


class TrafficViolationComparedMyColission(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_organisor': True})
    assign_team = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    date_received = models.DateField(null=True, blank=True)
    involved = models.CharField(max_length=2300, null=True)
    res_procedure = models.CharField(max_length=2300, null=True)

    comment = models.CharField(max_length=2300, blank=True, null=True)
    file_res = models.CharField(max_length=2300, blank=True, null=True)
    pdf = models.FileField(null=True, blank=True, upload_to='pdfs/TrafficViolationComparedMyColission/')

    status_track = models.BooleanField(default=False)


class ComplaintAndOfficeToAttend(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_organisor': True})
    assign_team = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    filed = models.CharField(max_length=2300, null=True)
    date_received = models.DateField(null=True, blank=True)
    affair = models.CharField(max_length=2300, null=True)

    comment = models.CharField(max_length=2300, blank=True, null=True)
    file_res = models.CharField(max_length=2300, blank=True, null=True)
    pdf = models.FileField(null=True, blank=True, upload_to='pdfs/ComplaintAndOfficeToAttend/')

    status_track = models.BooleanField(default=False)


class File2Return2dOffice(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_organisor': True})
    assign_team = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    filed = models.CharField(max_length=2300, null=True)
    guy = models.DateField(null=True, blank=True)
    involved = models.CharField(max_length=2300, null=True)

    comment = models.CharField(max_length=2300, blank=True, null=True)
    file_res = models.CharField(max_length=2300, blank=True, null=True)
    pdf = models.FileField(null=True, blank=True, upload_to='pdfs/File2Return2dOffice/')

    status_track = models.BooleanField(default=False)


class FilterSelection(models.Model):
    car_num = models.CharField(max_length=310)
    assign_team = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    filename = models.CharField(null=True, blank=True, max_length=255)
    filename2 = models.CharField(null=True, blank=True, max_length=255)
    agent_signature = models.BooleanField(default=False)
    organizer_signature = models.BooleanField(default=False)
    selected_urban_control_ids = models.TextField()
    selected_police_compliant_ids = models.TextField()
    selected_policeSubmissionLGGS_ids = models.TextField()
    selected_trafficViolationCompared_ids = models.TextField()
    selected_trafficViolationComparedMyColission_ids = models.TextField()
    selected_complaintAndOfficeToAttend_ids = models.TextField()
    selected_file2Return2dOffice_ids = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.car_num or ''


class InspNotifify(models.Model):
    msg = models.CharField(max_length=1000)
    createdAt = models.DateField(auto_now_add=True)
    assign_team = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.msg or ''


class CarNumber(models.Model):
    name = models.CharField(max_length=310)

    def __str__(self):
        return self.name


class UploadSignedPDF(models.Model):
    car_num = models.CharField(max_length=310)
    assign_team = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    pdf_file1 = models.FileField(null=True, blank=True, upload_to='pdfs/SignedPDF/')
    pdf_file2 = models.FileField(null=True, blank=True, upload_to='pdfs/SignedPDF/')
    createdAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.car_num
    