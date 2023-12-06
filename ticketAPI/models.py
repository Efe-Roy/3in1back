from django.db import models
from Auth.models import User
from contratacionAPI.models import resSecType

# Create your models here.
class Ticket(models.Model):
    STATE_TO_APPROVE = "to_approve"
    STATE_APPROVED = "approved"
    STATE_CLOSED = "closed"
    STATE_NOTABUG = "not_a_bug"
    STATE_WONTFIX = "wontfix"
    STATES = (
        (STATE_TO_APPROVE, "To Approve"),
        (STATE_APPROVED, "Approved"),
        (STATE_CLOSED, "Closed"),
        (STATE_NOTABUG, "Not a Bug"),
        (STATE_WONTFIX, "Won't fix"),
    )

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    subject = models.CharField(max_length=40, null=False, blank=False, default=None)
    description = models.TextField(blank=True)
    state = models.CharField(max_length=10, choices=STATES, default=STATE_TO_APPROVE)
    created_on = models.DateTimeField(auto_now_add=True)
    last_update_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject or ''
    