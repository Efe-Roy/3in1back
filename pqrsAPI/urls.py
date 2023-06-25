from django.urls import path
from .views import (
get_all_entityType, get_all_nameType, 
get_post_pqrs, get_details_pqrs, get_all_pqrs2, CurrentFileNumView,
FileResNumView, get_all_mediumRes, In_Form_pqrs
)

urlpatterns = [
    path('all_nameType', get_all_nameType.as_view()),
    path('all_entityType', get_all_entityType.as_view()),
    path('all_mediumRes', get_all_mediumRes.as_view()),
    path('all_pqrs', get_post_pqrs.as_view()),
    path('all_pqrs2', get_all_pqrs2.as_view()),
    path('pqrs_ById/<pk>/', get_details_pqrs.as_view()),

    path('get_filenum', CurrentFileNumView.as_view()),
    path('get_fileRes', FileResNumView.as_view()),
    path('post_inpqrs/<pk>/', In_Form_pqrs.as_view())
]
