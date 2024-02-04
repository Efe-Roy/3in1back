from django.urls import path
from .views import (
    PoliceCompliantView, PoliceCompliantDetailView, PoliceCompliantPrivateView, PoliceCompliantListView,
    UrbanControlView, UrbanControlDetailView, UrbanControlPrivateView, UrbanControlListView, 
    PoliceSubmissionLGGSView, PoliceSubmissionLGGSDetailView, PoliceSubmissionLGGSPrivateView, PoliceSubmissionLGGSListView,
    TrafficViolationComparedView, TrafficViolationComparedDetailView, TrafficViolationComparedPrivateView, TrafficViolationComparedListView,
    TrafficViolationComparedMyColissionListView, TrafficViolationComparedMyColissionView, TrafficViolationComparedMyColissionDetailView, TrafficViolationComparedMyColissionPrivateView,
    ComplaintAndOfficeToAttendListView, ComplaintAndOfficeToAttendView, ComplaintAndOfficeToAttendDetailView, ComplaintAndOfficeToAttendPrivateView,
    File2Return2dOfficeListView, File2Return2dOfficeView, File2Return2dOfficeDetailView, File2Return2dOfficePrivateView, InspNotifyView,
    UploadPDFView, UltimateView, InspUserListView, CarNum, ToggleSignature, ListUpdateAndEmailPDFView,
    CountAllInspResView,
    FilterDataView, FilteredDataDetailUpdateView, ListSelectedFilteredData, FilterSelectCreateView
)

urlpatterns = [
    path('police_compliant_list/', PoliceCompliantListView.as_view()),
    path('police_compliant', PoliceCompliantView.as_view()),
    path('police_compliant/<pk>/', PoliceCompliantDetailView.as_view()),
    path('police_compliant/private/<pk>/', PoliceCompliantPrivateView.as_view()),

    path('urban_control_list/', UrbanControlListView.as_view()),
    path('urban_control', UrbanControlView.as_view()),
    path('urban_control/<pk>/', UrbanControlDetailView.as_view()),
    path('urban_control/private/<pk>/', UrbanControlPrivateView.as_view()),

    path('police_submission_list/', PoliceSubmissionLGGSListView.as_view()),
    path('police_submission', PoliceSubmissionLGGSView.as_view()),
    path('police_submission/<pk>/', PoliceSubmissionLGGSDetailView.as_view()),
    path('police_submission/private/<pk>/', PoliceSubmissionLGGSPrivateView.as_view()),

    path('traffic_violation_compared_list/', TrafficViolationComparedListView.as_view()),
    path('traffic_violation_compared', TrafficViolationComparedView.as_view()),
    path('traffic_violation_compared/<pk>/', TrafficViolationComparedDetailView.as_view()),
    path('traffic_violation_compared/private/<pk>/', TrafficViolationComparedPrivateView.as_view()),

    path('traffic_violation_compared_colission_list/', TrafficViolationComparedMyColissionListView.as_view()),
    path('traffic_violation_compared_colission', TrafficViolationComparedMyColissionView.as_view()),
    path('traffic_violation_compared_colission/<pk>/', TrafficViolationComparedMyColissionDetailView.as_view()),
    path('traffic_violation_compared_colission/private/<pk>/', TrafficViolationComparedMyColissionPrivateView.as_view()),

    path('complaint_Office2attend_list/', ComplaintAndOfficeToAttendListView.as_view()),
    path('complaint_Office2attend', ComplaintAndOfficeToAttendView.as_view()),
    path('complaint_Office2attend/<pk>/', ComplaintAndOfficeToAttendDetailView.as_view()),
    path('complaint_Office2attend/private/<pk>/', ComplaintAndOfficeToAttendPrivateView.as_view()),

    path('file2return2doffice_list/', File2Return2dOfficeListView.as_view()),
    path('file2return2doffice', File2Return2dOfficeView.as_view()),
    path('file2return2doffice/<pk>/', File2Return2dOfficeDetailView.as_view()),
    path('file2return2doffice/private/<pk>/', File2Return2dOfficePrivateView.as_view()),



    # path('autogen', AutoGenView.as_view()),


    path('count_all_insp_res', CountAllInspResView.as_view()),
    path('insp_notify', InspNotifyView.as_view()),
    path('ultimate/<int:pk>/', UltimateView.as_view(), name='ultimate-view'),

    path('upload/', UploadPDFView.as_view(), name='upload-pdf'),
    path('insp_userlist/', InspUserListView.as_view()),

    path('carnum/', CarNum.as_view()),
    path('toggle_signature/<int:selection_id>/', ToggleSignature.as_view()),
    path('list-pdf/', ListUpdateAndEmailPDFView.as_view()),

    # New
    path('post_filter/', FilterSelectCreateView.as_view()),
    path('filter_test/', FilterDataView.as_view()),
    path('list_filtered_selected/', ListSelectedFilteredData.as_view()),
    path('filter_detail/<int:selection_id>/', FilteredDataDetailUpdateView.as_view(), name='filtered_data'),
]
