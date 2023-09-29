from django.urls import path
from .views import get_sisben

urlpatterns = [
    path('get_sisben/', get_sisben.as_view()),
]
