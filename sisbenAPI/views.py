import concurrent.futures
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ( ListCreateAPIView, ListAPIView )
from .serializers import SisbenMainSerializer, LocationTypeSerializer, SisbenMainSerializer2
from .models import SisbenMain, LocationType
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from django.http import Http404
from rest_framework.views import APIView
from twilio.rest import Client
from django.conf import settings
from django.template.loader import render_to_string
from multiprocessing import Pool
from multiprocessing import cpu_count
import time
from twilio.base.exceptions import TwilioRestException

# Create your views here.
class CustomPagination(PageNumberPagination):
    page_size_query_param = 'PageSize'
    # max_page_size = 100

class get_sisben(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SisbenMainSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = SisbenMain.objects.all().order_by("-id")

        # Filter based on request parameters
        full_name = self.request.query_params.get('full_name', None)
        if full_name:
            queryset = queryset.filter(full_name__icontains=full_name)
   
        citizenship_card = self.request.query_params.get('citizenship_card', None)
        if citizenship_card:
            queryset = queryset.filter(citizenship_card__icontains=citizenship_card)
   
        return queryset


class post_sisben(APIView):
    def post(self, request, format=None):
        serializer = SisbenMainSerializer2(data=request.data)
        if serializer.is_valid():
            serializer.save()
           
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class detail_update_sisben(APIView):
    def get_object(self, pk):
        try:
            return SisbenMain.objects.get(id=pk)
        except SisbenMain.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        SisbenById = self.get_object(pk)
        serializer = SisbenMainSerializer(SisbenById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        SisbenById = self.get_object(pk)
        serializer = SisbenMainSerializer2(SisbenById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     PqrsById = self.get_object(pk)
    #     PqrsById.delete()
    #     return Response(status= HTTP_204_NO_CONTENT)

class get_all_location(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LocationTypeSerializer
    queryset = LocationType.objects.all()

@api_view(['POST'])
def delete_data(request):
    try:
        # Delete all records from the table
        SisbenMain.objects.all().delete()
        return Response({'message': 'All data deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SendWhatsAppMessage(APIView):
    def post(self, request):
        recipient_phone_number = request.POST.get('recipient_phone_number')

        dynamic_data = {
            'recipient_name': 'John Doe',
            'appointment_date': '2023-10-10',
            'appointment_time': '15:00',
        }
        message_body = render_to_string('twilo/whatsapp.txt', dynamic_data)
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        try:
            message = client.messages.create(
                body=message_body,
                from_=settings.TWILIO_WHATSAPP_NUMBER,
                to=f"whatsapp:{recipient_phone_number}"
            )
            print(message.sid)
            return Response({'message': 'WhatsApp message sent successfully'})
        except Exception as e:
            return Response({'message': str(e)}, status=500)
           
# http://your-django-server/api_endpoint/
# class SendBulkWhatsAppMessages(APIView):
#     def post(self, request):
#         try:
#             cell_phones = SisbenMain.objects.all().values_list('cell_phone', flat=True)
#             success_count, failure_count = self.send_bulk_whatsapp_messages(cell_phones)

#             return Response({
#                 'success_count': success_count,
#                 'failure_count': failure_count,
#             })
#         except Exception as e:
#             return Response({'message': str(e)}, status=500)

#     def send_whatsapp_message(self, recipient_phone_number):
#         dynamic_data = {
#             'recipient_name': 'John Doe',
#             'appointment_date': '2023-10-10',
#             'appointment_time': '15:00',
#         }
#         message_body = render_to_string('twilo/whatsapp2.txt', dynamic_data)
#         client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

#         try:
#             message = client.messages.create(
#                 body=message_body,
#                 from_=settings.TWILIO_WHATSAPP_NUMBER,
#                 to=f"whatsapp:{recipient_phone_number}"
#             )
#             print(f"Message sent to {recipient_phone_number}. SID: {message.sid}")
#             return True
#         except Exception as e:
#             print(f"Failed to send message to {recipient_phone_number}: {str(e)}")
#             return False

#     def send_bulk_whatsapp_messages(self, recipient_phone_numbers):
#         num_processes = 4  # Adjust based on your server's capacity

#         with Pool(num_processes) as pool:
#             results = pool.map(self.send_whatsapp_message, recipient_phone_numbers)

#         success_count = sum(results)
#         failure_count = len(recipient_phone_numbers) - success_count

#         return success_count, failure_count
    
# class SendBulkWhatsAppMessages(APIView):
#     def post(self, request):
#         try:
#             sisben_records = SisbenMain.objects.all()
#             success_count, failure_count = self.send_bulk_whatsapp_messages(sisben_records)

#             return Response({
#                 'success_count': success_count,
#                 'failure_count': failure_count,
#             })
#         except Exception as e:
#             return Response({'message': str(e)}, status=500)

#     def send_whatsapp_message(self, sisben_record):
#         message_body = render_to_string('twilo/whatsapp2.txt')
#         client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

#         try:
#             message = client.messages.create(
#                 body=message_body,
#                 from_=settings.TWILIO_WHATSAPP_NUMBER,
#                 to=f"whatsapp:+57{sisben_record.cell_phone}"
#             )
#             print(f"Message sent to {sisben_record.cell_phone}. SID: {message.sid}")
#             return True
#         except Exception as e:
#             print(f"Failed to send message to {sisben_record.cell_phone}: {str(e)}")
#             return False

#     def send_bulk_whatsapp_messages(self, sisben_records):
#         num_processes = 4  # Adjust based on your server's capacity

#         with Pool(num_processes) as pool:
#             results = pool.map(self.send_whatsapp_message, sisben_records)

#         success_count = sum(results)
#         failure_count = len(sisben_records) - success_count

#         return success_count, failure_count

# class SendBulkWhatsAppMessages(APIView):
#     def post(self, request):
#         try:
#             sisben_records = SisbenMain.objects.all()
#             success_count, failure_count = self.send_bulk_whatsapp_messages(sisben_records)

#             return Response({
#                 'success_count': success_count,
#                 'failure_count': failure_count,
#             })
#         except Exception as e:
#             return Response({'message': str(e)}, status=500)

#     def send_whatsapp_message(self, sisben_record, message_body):
#         try:
#             client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#             to_number = f"whatsapp:+57{sisben_record.cell_phone}"
            
#             message = client.messages.create(
#                 body=message_body,
#                 from_=settings.TWILIO_WHATSAPP_NUMBER,
#                 to=to_number
#             )
            
#             print(f"Message sent to {to_number}. SID: {message.sid}")
#             return True
#         except Exception as e:
#             print(f"Failed to send message to {to_number}: {str(e)}")
#             # Add rate limiting: wait for 1 second before the next request
#             time.sleep(1)

#         return False

#     def send_bulk_whatsapp_messages(self, sisben_records):
#         num_processes = cpu_count()  # Use the number of CPU cores available
        
#         # Render the message body outside the parallelized section
#         dynamic_data = {
#             'recipient_name': 'John Doe',
#             'appointment_date': '2023-10-10',
#             'appointment_time': '15:00',
#         }
#         message_body = render_to_string('twilo/whatsapp2.txt', dynamic_data)

#         # Use ThreadPoolExecutor for parallelization
#         with concurrent.futures.ThreadPoolExecutor(max_workers=num_processes) as executor:
#             futures = [executor.submit(self.send_whatsapp_message, record, message_body) for record in sisben_records]

#         success_count = sum(f.result() for f in futures)
#         failure_count = len(sisben_records) - success_count

#         return success_count, failure_count
    

class SendBulkWhatsAppMessages(APIView):
    def post(self, request):
        try:
            sisben_records = SisbenMain.objects.all()
            success_count, failure_count = self.send_bulk_whatsapp_messages(sisben_records)

            return Response({
                'success_count': success_count,
                'failure_count': failure_count,
            })
        except Exception as e:
            return Response({'message': str(e)}, status=500)

    def send_whatsapp_message(self, sisben_record, message_body):
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            to_number = f"whatsapp:+57{sisben_record.cell_phone}"
            
            message = client.messages.create(
                body=message_body,
                from_=settings.TWILIO_WHATSAPP_NUMBER,
                to=to_number
            )
            
            print(f"Message sent to {to_number}. SID: {message.sid}")
            return True
        except TwilioRestException as e:
            if e.code == 429:  # Twilio's rate limit exceeded (HTTP 429 Too Many Requests)
                # Implement exponential backoff with retries
                max_retries = 5
                retry_delay = 1  # seconds
                for retry_count in range(max_retries):
                    print(f"Rate limit exceeded. Retrying in {retry_delay} seconds (Retry {retry_count + 1}/{max_retries})...")
                    time.sleep(retry_delay)
                    try:
                        # Retry sending the message
                        message = client.messages.create(
                            body=message_body,
                            from_=settings.TWILIO_WHATSAPP_NUMBER,
                            to=to_number
                        )
                        print(f"Message sent to {to_number}. SID: {message.sid}")
                        return True
                    except TwilioRestException as e:
                        if e.code != 429:
                            print(f"Failed to send message to {to_number}: {str(e)}")
                print(f"Max retry attempts reached. Failed to send message to {to_number}.")
            else:
                print(f"Failed to send message to {to_number}: {str(e)}")
        except Exception as e:
            print(f"Failed to send message to {to_number}: {str(e)}")
    
        return False

    def send_bulk_whatsapp_messages(self, sisben_records):
        message_body = render_to_string('twilo/whatsapp2.txt')

        success_count = 0
        failure_count = 0

        for sisben_record in sisben_records:
            if self.send_whatsapp_message(sisben_record, message_body):
                success_count += 1
            else:
                failure_count += 1

        return success_count, failure_count

