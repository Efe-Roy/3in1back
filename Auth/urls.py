from .views import SignupView
from django.urls import path, include
from .views import (
    CustomAuthToken, UserListView, UserDetail, 
    get_all_team, UserProfileUpdate, UserProfileDetail,
    CreateOperatorView, get_all_agent
)

urlpatterns = [
    path('api/rest-auth/registration/', SignupView.as_view()),
    path('api/rest-auth/login/', CustomAuthToken.as_view(), name ='auth-token'),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/userlist', UserListView.as_view()),
    path('api/users/<int:pk>/', UserDetail.as_view()),

    path('api/create-operators', CreateOperatorView.as_view()),

    path('api/userprofile/<int:pk>/', UserProfileDetail.as_view()),
    path('api/users/update/', UserProfileUpdate.as_view()), #still under testing

    path('api/teams', get_all_team.as_view()),
    path('api/agent', get_all_agent.as_view()),
]

