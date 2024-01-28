from django.urls import path
from .views import (
get_all_entityType, get_all_nameType, DashboardView,
get_post_pqrs, get_details_pqrs, get_all_pqrs2, CurrentFileNumView,
FileResNumView, get_all_mediumRes, In_Form_pqrs, get_pqrs, get_all_statuType, PqrsNotifyView
)

urlpatterns = [
    path('all_nameType', get_all_nameType.as_view()),
    path('all_entityType', get_all_entityType.as_view()),
    path('all_mediumRes', get_all_mediumRes.as_view()),
    path('all_statuType', get_all_statuType.as_view()),
    path('all_pqrs', get_post_pqrs.as_view()),
    path('get_pqrs/', get_pqrs.as_view()),
    path('all_pqrs2', get_all_pqrs2.as_view()),
    path('pqrs_ById/<pk>/', get_details_pqrs.as_view()),

    path('get_filenum', CurrentFileNumView.as_view()),
    path('get_fileRes', FileResNumView.as_view()),
    path('post_inpqrs/<pk>/', In_Form_pqrs.as_view()),

    path('dashboard', DashboardView.as_view()),

    path('pqrs_notify', PqrsNotifyView.as_view()),
]
