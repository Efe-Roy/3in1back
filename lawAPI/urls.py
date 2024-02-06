from django.urls import path
from .views import get_post_prev_stud, PrevStudListView

urlpatterns = [
    path('get_post_prev_stud/', get_post_prev_stud.as_view()),
    path('list_prev_stud/', PrevStudListView.as_view()),
]
