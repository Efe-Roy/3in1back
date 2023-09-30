from django.urls import path
from .views import get_sisben, delete_data, post_sisben, get_all_location

urlpatterns = [
    path('get_sisben/', get_sisben.as_view()),
    path('post_sisben/', post_sisben.as_view()),
    path('get_location/', get_all_location.as_view()),
    path('delete_data/', delete_data, name='delete_data'),
]
