from django.urls import path
from .views import (
    get_all_processType, get_all_acroymsType, get_all_typologyType, 
    get_all_resSecType, get_all_StateType, get_post_contratacion, 
    get_details_contratacion, get_contratacion,get_filtered_contratacion, 
    NotificationView, ListUnusedValueAdded, get_prerequisite, LawFirmView,
    create_contratacion, get_base, update_prerequisite, ActivateDeactivateContrataction,
    UpdateEmptyStateAPIView, test_contratacion, get_contratacion_dashboard
)

urlpatterns = [
    path('all_processType', get_all_processType.as_view()),
    path('all_acroymsType', get_all_acroymsType.as_view()),
    path('all_typologyType', get_all_typologyType.as_view()),
    path('all_resSecType', get_all_resSecType.as_view()),
    path('all_StateType', get_all_StateType.as_view()),

    path('active_deactive_contratacion/<int:pk>/', ActivateDeactivateContrataction.as_view()),
    path('get_contratacion_dashboard/', get_contratacion_dashboard.as_view()),
    path('get_contratacion/', get_contratacion.as_view()),
    path('test_contratacion/', test_contratacion.as_view()),
    path('get_filtered_contratacion/', get_filtered_contratacion.as_view()),
    path('get_prerequisite/<ptR>/<acR>/<rscR>/', get_prerequisite.as_view()),
    path('update_prerequisite/<ptR>/<acR>/<rscR>/<int:pk>/', update_prerequisite.as_view()),
    path('get_base/<ptR>/<rscR>/', get_base.as_view()),
    
    path('create_contratacion', create_contratacion.as_view()),
    path('get_post_contratacion', get_post_contratacion.as_view()),
    path('get_detail_contratacion/<pk>/', get_details_contratacion.as_view()),

    path('notifications', NotificationView.as_view()),
    path('list-value-added/', ListUnusedValueAdded.as_view()),

    path('lawfirm/<pk>/', LawFirmView.as_view()),


    path('update_empty_state/', UpdateEmptyStateAPIView.as_view()),

]

