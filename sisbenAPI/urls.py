from django.urls import path
from .views import get_sisben, delete_data, post_sisben, get_all_location, detail_update_sisben, SendWhatsAppMessage, SendBulkWhatsAppMessages, broadcast_sms

urlpatterns = [
    path('get_sisben/', get_sisben.as_view()),
    path('post_sisben/', post_sisben.as_view()),
    path('detail_update/<pk>/', detail_update_sisben.as_view()),
    path('get_location/', get_all_location.as_view()),
    path('delete_data/', delete_data, name='delete_data'),
    path('send_whatsapp/', SendWhatsAppMessage.as_view()),
    path('send_bulk_whatsapp/', SendBulkWhatsAppMessages.as_view()),

    path(r'broadcast', broadcast_sms, name="default"),
]
