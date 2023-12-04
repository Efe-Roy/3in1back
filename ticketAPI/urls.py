from django.urls import path
from .views import (
    TicketView, TicketViewById
)

urlpatterns = [
    path('', TicketView.as_view()),
    path('<int:pk>/', TicketViewById.as_view())
]

