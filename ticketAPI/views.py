from django.shortcuts import render
from django.http import Http404
from django.db.models import Count
from .models import Ticket, TicketUserAgent
from Auth.models import TicketUserAgent, User
from .serializers import TicketSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import datetime

# Create your views here.
class CustomPagination(PageNumberPagination):
    page_size_query_param = 'PageSize'

class TicketView(generics.ListCreateAPIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        # queryset = Ticket.objects.all().order_by('-id')

        user = self.request.user
        # print("qaws", user.is_organisor)
        if user.is_organisor:
            queryset = Ticket.objects.all().order_by('-id')
        elif user.is_ticket_agent:
            foundObject = TicketUserAgent.objects.get(user_id=user.id)
            ticket_agent = foundObject.id
            queryset = Ticket.objects.filter(assign_to_agent=ticket_agent).order_by('-id')
        else:
            queryset = Ticket.objects.filter(user=user).order_by('-id')
        

        # Filter based on request parameters
        responsible_secretary = self.request.query_params.get('responsible_secretary', None)
        if responsible_secretary:
            queryset = queryset.filter(responsible_secretary__name__icontains=responsible_secretary)

        state = self.request.query_params.get('state', None)
        if state:
            queryset = queryset.filter(state=state)

        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Count instances of each stateType
        state_counts = queryset.values('state').annotate(state_count=Count('state'))
        # Sum the counts for each state
        # total_state_counts = {state['state']: state['state_count'] for state in state_counts}
        total_state_counts = {}
        for state in state_counts:
            total_state_counts[state['state']] = total_state_counts.get(state['state'], 0) + state['state_count']


        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = {
                'results': serializer.data,
                'state_counts': total_state_counts
            }
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'results': serializer.data,
            'state_counts': total_state_counts
        }

        return Response(response_data)
    
    def create(self, request, *args, **kwargs):
        generate_automated_number = self.generate_automated_number()
        # print("generate_automated_number", generate_automated_number)
        modified_data = self.modify_request_data(request.data)
        serializer = self.get_serializer(data=modified_data)
        # serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = self.request.user
        serializer.validated_data['ticket_num'] = generate_automated_number

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def modify_request_data(self, data):
        modified_data = data.copy()
        if 'image[]' in modified_data:
            modified_data['image'] = modified_data.pop('image[]')[0]  # Extract the first element
        return modified_data
    
    def generate_automated_number(self):
        get_ticket = Ticket.objects.all()
        year = datetime.now().year

        if get_ticket.exists():
            last_ticket = Ticket.objects.all().order_by('-id')[0]
            string = last_ticket.ticket_num
            parts = string.split("-")
            number = parts[0]
            # print(number)
            file_num = int(number) + 1
            d = "%04d" % ( file_num, ) + f'-{year}'
            # print(d)
            return d
        else:
            # print("Empty")
            file_num = 1
            d = "%04d" % ( file_num, ) + f'-{year}'
            # print(d)
            return d
    
class TicketViewById(APIView):
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, pk):
        try:
            return Ticket.objects.get(id=pk)
        except Ticket.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        querysetById = self.get_object(pk)
        serializer = TicketSerializer(querysetById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        querysetById = self.get_object(pk)
        serializer = TicketSerializer(querysetById, data=request.data)
        assign_to_agent = request.data.get("assign_to_agent", None)

        foundObject = None
        if assign_to_agent:
            try:
                foundObject = TicketUserAgent.objects.get(user_id=assign_to_agent)
                # print("foundObject", foundObject)
            except TicketUserAgent.DoesNotExist:
                return Response({"assign_to_agent": ["Invalid user ID"]}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            if assign_to_agent:
                serializer.validated_data['assign_to_agent'] = foundObject

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        querysetById = self.get_object(pk)
        querysetById.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    
