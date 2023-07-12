from django.urls import path
from .views import (
    PoliceCompliantView, PoliceCompliantDetailView, PoliceCompliantPrivateView, 
    UrbanControlView, UrbanControlDetailView, UrbanControlPrivateView, 
    PoliceSubmissionLGGSView, PoliceSubmissionLGGSDetailView, PoliceSubmissionLGGSPrivateView,
    TrafficViolationComparedView, TrafficViolationComparedDetailView, TrafficViolationComparedPrivateView,
    TrafficViolationComparedMyColissionView, TrafficViolationComparedMyColissionDetailView, TrafficViolationComparedMyColissionPrivateView,
    ComplaintAndOfficeToAttendView, ComplaintAndOfficeToAttendDetailView, ComplaintAndOfficeToAttendPrivateView,
    File2Return2dOfficeView, File2Return2dOfficeDetailView, File2Return2dOfficePrivateView
)

urlpatterns = [
    path('police_compliant', PoliceCompliantView.as_view()),
    path('police_compliant/<pk>/', PoliceCompliantDetailView.as_view()),
    path('police_compliant/private/<pk>/', PoliceCompliantPrivateView.as_view()),

    path('urban_control', UrbanControlView.as_view()),
    path('urban_control/<pk>/', UrbanControlDetailView.as_view()),
    path('urban_control/private/<pk>/', UrbanControlPrivateView.as_view()),

    path('police_submission', PoliceSubmissionLGGSView.as_view()),
    path('police_submission/<pk>/', PoliceSubmissionLGGSDetailView.as_view()),
    path('police_submission/private/<pk>/', PoliceSubmissionLGGSPrivateView.as_view()),

    path('traffic_violation_compared', TrafficViolationComparedView.as_view()),
    path('traffic_violation_compared/<pk>/', TrafficViolationComparedDetailView.as_view()),
    path('traffic_violation_compared/private/<pk>/', TrafficViolationComparedPrivateView.as_view()),

    path('traffic_violation_compared_colission', TrafficViolationComparedMyColissionView.as_view()),
    path('traffic_violation_compared_colission/<pk>/', TrafficViolationComparedMyColissionDetailView.as_view()),
    path('traffic_violation_compared_colission/private/<pk>/', TrafficViolationComparedMyColissionPrivateView.as_view()),

    path('complaint_Office2attend', ComplaintAndOfficeToAttendView.as_view()),
    path('complaint_Office2attend/<pk>/', ComplaintAndOfficeToAttendDetailView.as_view()),
    path('complaint_Office2attend/private/<pk>/', ComplaintAndOfficeToAttendPrivateView.as_view()),

    path('file2return2doffice', File2Return2dOfficeView.as_view()),
    path('file2return2doffice/<pk>/', File2Return2dOfficeDetailView.as_view()),
    path('file2return2doffice/private/<pk>/', File2Return2dOfficePrivateView.as_view()),
]
