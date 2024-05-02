from django.urls import path
from .views import ( 
    get_post_prev_stud, PrevStudListView,
    OperationView, OperationDetailView, OperationListView
)
urlpatterns = [
    path('get_post_prev_stud/', get_post_prev_stud.as_view()),
    path('list_prev_stud/', PrevStudListView.as_view()),
    
    path('operation/', OperationView.as_view()),
    path('operation_list/', OperationListView.as_view()),
    path('operation/<pk>/', OperationDetailView.as_view()),
]
