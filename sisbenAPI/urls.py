from django.urls import path
from .views import get_sisben, delete_data

urlpatterns = [
    path('get_sisben/', get_sisben.as_view()),
    path('delete_data/', delete_data, name='delete_data'),
]
