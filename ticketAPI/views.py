from django.shortcuts import render
from django.http import Http404
from django.db.models import Count
from .models import Ticket, TicketUserAgent
from .serializers import TicketSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

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
        # Modify only the 'image[]' key in the request data
        modified_data = request.data.copy()
        if 'image[]' in modified_data:
            modified_data['image'] = modified_data.pop('image[]')[0]
        
        # print("modified_data", modified_data)
        # print("form data", request.data)
        serializer = self.get_serializer(data=modified_data)

        # serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = self.request.user


        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        querysetById = self.get_object(pk)
        querysetById.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    
