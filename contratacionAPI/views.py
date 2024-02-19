from django.shortcuts import render
from django.db.models import Max
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView, ListCreateAPIView
)
from .serializers import (
    ContratacionMainSerializer, ProcessTypeSerializer, AcroymsTypeSerializer,
    TypologyTypeSerializer, ResSecTypeSerializer, StateTypeSerializer, AllContratacionMainSerializer,
    NotificationSerializer, ValueAddedSerializer, LawFirmSerializer, PlanContratacionMainSerializer
    )
from Auth.models import ActivityTracker
from .models import (
    ValueAdded, BpinProjectCode, ValueAffectedBpinProjCDP, BudgetItems, ArticleName, ItemValue,
    ContratacionMain, processType, acroymsType, typologyType, resSecType, StateType, Notification,
    LawFirmModel
)
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.authentication import TokenAuthentication
import re
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum, F, DecimalField, Count, IntegerField, Case, When, Value, CharField, Func, ExpressionWrapper
from django.db.models.functions import Cast, Substr
from decimal import Decimal
from datetime import datetime
from .namesTitle import NAMES

# def jsonRoy(request):
#     data= list(ContratacionMain.objects.values())
#     return JsonResponse(data, safe=False)

class get_all_processType(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProcessTypeSerializer
    queryset = processType.objects.all()

class get_all_acroymsType(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AcroymsTypeSerializer
    queryset = acroymsType.objects.all()

class get_all_typologyType(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TypologyTypeSerializer
    queryset = typologyType.objects.all()

class get_all_resSecType(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResSecTypeSerializer
    queryset = resSecType.objects.all()

class get_all_StateType(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = StateTypeSerializer
    queryset = StateType.objects.all()
    
# ======Start One Family type of logic but different purpose =======
class update_prerequisite(APIView):
    def get(self, request, ptR, acR, rscR, pk):
        pt = processType.objects.get(id=ptR)
        ac = acroymsType.objects.get(id=acR)
        rsc = resSecType.objects.get(id=rscR)
        instance_obj = ContratacionMain.objects.get(id=pk)
        # print("pk pk:-", pk)

        rsc_order = {
            'AMS': "ALCALDÍA MUNICIPAL",
            'SGG': "SECRETARÍA GENERAL Y DE GOBIERNO",
            'SPO': "SECRETARÍA DE PLANEACIÓN Y ORDENAMIENTO TERRITORIAL",
            'SHB': "SECRETARÍA DE HACIENDA Y BIENES",
            'SIE': "SECRETARÍA DE INNOVACIÓN Y EMPRENDIMIENTO",
            'SPD': "SECRETARÍA DE PROTECCIÓN SOCIAL Y DESARROLLO COMUNITARIO",
            'SSP': "SECRETARÍA DE SERVICIOS PÚBLICOS Y MEDIO AMBIENTE",
        }

        pt_order = {
            'MC': "CONTRATACIÓN MÍNIMA CUANTÍA.",
            'SAMC': "SELECCIÓN ABREVIADA DE MENOR CUANTÍA",
            'SI': "SUBASTA INVERSA",
            'LP': "LICITACIÓN PÚBLICA",
            'CM': "CONCURSO DE MÉRITOS",
            'CD': "CONTRATACIÓN DIRECTA",
        }
        
        result = "Unknown"
        if rsc.name in rsc_order.values():
            # Find the key for the given name
            result = next(key for key, value in rsc_order.items() if value == rsc.name)
        
        result_pt = "Unknown"
        if pt.name in pt_order.values():
            # Find the key for the given name
            result_pt = next(key for key, value in pt_order.items() if value == pt.name)

        if pt.name == "CONTRATACIÓN DIRECTA":
            initial_part = f'{result_pt}-{ac.name}-{result}'
        else:
            initial_part = f'{result_pt}-{result}'
        
        automated_number = self.update_automated_number(initial_part, instance_obj)

        return Response(automated_number)
    
    def update_automated_number(cls, initial_part, instance_obj):
        # print("inside auto", instance_obj.id)
        year = datetime.now().year
        filtered_objects = ContratacionMain.objects.filter(process_num__startswith=initial_part)
        if filtered_objects.exists():
            highest_value = filtered_objects.aggregate(Max('process_num'))['process_num__max']
            print("highest_value", highest_value.split('-')[-1])

            if highest_value is not None:
                # Extract the numeric part from the 'process_num' field
                year_part = int(highest_value.split('-')[-1])
                if year_part >= year:
                    numeric_part = int(highest_value.split('-')[-2])
                    count_str_0 = str(numeric_part).zfill(3)
                    plus_1 = numeric_part + 1
                    count_str_1 = str(plus_1).zfill(3)

                    d_d = f'{initial_part}-{count_str_0}-{year}'
                    objjj = ContratacionMain.objects.get(process_num=d_d)
                    # return f'{instance_obj.process_num}'
                    if objjj is not None and instance_obj.process_num == d_d:
                        return f'{initial_part}-{count_str_0}-{year}'
                    else:
                        return f'{initial_part}-{count_str_1}-{year}'

                    # return f'{initial_part}-{count_str_1}-{year}'
                else:
                    return f'{initial_part}-001-{year}'
            else:
                return f'{initial_part}-001-{year}'
        else:
            return f'{initial_part}-001-{year}'
        
class get_prerequisite(APIView):
    def get(self, request, ptR, acR, rscR):
        pt = processType.objects.get(id=ptR)
        ac = acroymsType.objects.get(id=acR)
        rsc = resSecType.objects.get(id=rscR)

        rsc_order = {
            'AMS': "ALCALDÍA MUNICIPAL",
            'SGG': "SECRETARÍA GENERAL Y DE GOBIERNO",
            'SPO': "SECRETARÍA DE PLANEACIÓN Y ORDENAMIENTO TERRITORIAL",
            'SHB': "SECRETARÍA DE HACIENDA Y BIENES",
            'SIE': "SECRETARÍA DE INNOVACIÓN Y EMPRENDIMIENTO",
            'SPD': "SECRETARÍA DE PROTECCIÓN SOCIAL Y DESARROLLO COMUNITARIO",
            'SSP': "SECRETARÍA DE SERVICIOS PÚBLICOS Y MEDIO AMBIENTE",
        }

        pt_order = {
            'MC': "CONTRATACIÓN MÍNIMA CUANTÍA.",
            'SAMC': "SELECCIÓN ABREVIADA DE MENOR CUANTÍA",
            'SI': "SUBASTA INVERSA",
            'LP': "LICITACIÓN PÚBLICA",
            'CM': "CONCURSO DE MÉRITOS",
            'CD': "CONTRATACIÓN DIRECTA",
        }
        
        result = "Unknown"
        if rsc.name in rsc_order.values():
            # Find the key for the given name
            result = next(key for key, value in rsc_order.items() if value == rsc.name)
        
        result_pt = "Unknown"
        if pt.name in pt_order.values():
            # Find the key for the given name
            result_pt = next(key for key, value in pt_order.items() if value == pt.name)

        initial_part = f'{result_pt}-{ac.name}-{result}'
        
        automated_number = self.generate_automated_number(initial_part, ac, result)

        return Response(automated_number)
    
    def generate_automated_number(cls, initial_part, ac, result):
        year = datetime.now().year
        print(ac.name)
        filtered_objects = ContratacionMain.objects.filter(process_num__icontains=f'{ac.name}-{result}')
        filtered_objects_cno = ContratacionMain.objects.filter(contact_no__icontains=f'{ac.name}-{result}')
        if filtered_objects.exists() or filtered_objects_cno.exists():
            highest_value = filtered_objects.aggregate(Max('process_num'))['process_num__max']
            highest_contact_no = filtered_objects_cno.aggregate(Max('contact_no'))['contact_no__max']

            print(highest_value)
            # desired_highest_value = highest_value[3:] 
            # desired_highest_contact_no = highest_contact_no[3:] 
            
            desired_highest_value = highest_value[3:] if highest_value is not None else None
            desired_highest_contact_no = highest_contact_no[3:] if highest_contact_no is not None else None

            print("desired_highest_value", desired_highest_value)
            print("desired_highest_contact_no", desired_highest_contact_no)
            
            # Find the maximum number
            # max_number = max(desired_highest_value, desired_highest_contact_no)
            max_number = max(desired_highest_value or '', desired_highest_contact_no or '')

            # Now you can use this new highest number in your code
            # print("New highest number:", max_number)

            if max_number is not None:
                # Extract the numeric part from the 'process_num' field
                year_part = int(max_number.split('-')[-1])
                if year_part >= year:
                    numeric_part = int(max_number.split('-')[-2])
                    plus_1 = numeric_part + 1
                    count_str = str(plus_1).zfill(3)
                    return f'{initial_part}-{count_str}-{year}'
                else:
                    return f'{initial_part}-001-{year}'
            else:
                return f'{initial_part}-001-{year}'
        else:
            return f'{initial_part}-001-{year}'
        
class get_base(APIView):
    def get(self, request, ptR, rscR):
        pt = processType.objects.get(id=ptR)
        # ac = acroymsType.objects.get(id=acR)
        rsc = resSecType.objects.get(id=rscR)

        rsc_order = {
            'AMS': "ALCALDÍA MUNICIPAL",
            'SGG': "SECRETARÍA GENERAL Y DE GOBIERNO",
            'SPO': "SECRETARÍA DE PLANEACIÓN Y ORDENAMIENTO TERRITORIAL",
            'SHB': "SECRETARÍA DE HACIENDA Y BIENES",
            'SIE': "SECRETARÍA DE INNOVACIÓN Y EMPRENDIMIENTO",
            'SPD': "SECRETARÍA DE PROTECCIÓN SOCIAL Y DESARROLLO COMUNITARIO",
            'SSP': "SECRETARÍA DE SERVICIOS PÚBLICOS Y MEDIO AMBIENTE",
        }

        pt_order = {
            'MC': "CONTRATACIÓN MÍNIMA CUANTÍA.",
            'SAMC': "SELECCIÓN ABREVIADA DE MENOR CUANTÍA",
            'SI': "SUBASTA INVERSA",
            'LP': "LICITACIÓN PÚBLICA",
            'CM': "CONCURSO DE MÉRITOS",
            'CD': "CONTRATACIÓN DIRECTA",
        }
        
        result = "Unknown"
        if rsc.name in rsc_order.values():
            # Find the key for the given name
            result = next(key for key, value in rsc_order.items() if value == rsc.name)
        
        result_pt = "Unknown"
        if pt.name in pt_order.values():
            # Find the key for the given name
            result_pt = next(key for key, value in pt_order.items() if value == pt.name)

        if pt.name == "CONTRATACIÓN DIRECTA":
            initial_part = None
        else:
            initial_part = f'{result_pt}-{result}'
            
        # initial_part = f'{result_pt}-{result}'
        
        automated_number = self.generate_automated_number(initial_part)

        return Response(automated_number)
    
    def generate_automated_number(cls, initial_part):
        year = datetime.now().year
        filtered_objects = ContratacionMain.objects.filter(process_num__startswith=initial_part)
        if filtered_objects.exists():
            highest_value = filtered_objects.aggregate(Max('process_num'))['process_num__max']
            print("highest_value", highest_value.split('-')[-1])

            if highest_value is not None:
                # Extract the numeric part from the 'process_num' field
                year_part = int(highest_value.split('-')[-1])
                if year_part >= year:
                    numeric_part = int(highest_value.split('-')[-2])
                    plus_1 = numeric_part + 1
                    count_str = str(plus_1).zfill(3)
                    return f'{initial_part}-{count_str}-{year}'
                else:
                    return f'{initial_part}-001-{year}'
            else:
                return f'{initial_part}-001-{year}'
        else:
            return f'{initial_part}-001-{year}'
        
# ====== End One Family type of logic but different purpose =======


class create_contratacion(APIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        d_state = StateType.objects.get(id=request.data["state"])
        user = self.request.user
        # process_num = request.data["process_num"]
        pt = processType.objects.get(id=request.data["process"])
        rsc = resSecType.objects.get(id=request.data["responsible_secretary"])
        if request.data["acroyms_of_contract"]:
            ac = acroymsType.objects.get(id=request.data["acroyms_of_contract"])

        order = {
            'AMS': "ALCALDÍA MUNICIPAL",
            'SGG': "SECRETARÍA GENERAL Y DE GOBIERNO",
            'SPO': "SECRETARÍA DE PLANEACIÓN Y ORDENAMIENTO TERRITORIAL",
            'SHB': "SECRETARÍA DE HACIENDA Y BIENES",
            'SIE': "SECRETARÍA DE INNOVACIÓN Y EMPRENDIMIENTO",
            'SPD': "SECRETARÍA DE PROTECCIÓN SOCIAL Y DESARROLLO COMUNITARIO",
            'SSP': "SECRETARÍA DE SERVICIOS PÚBLICOS Y MEDIO AMBIENTE",
        }
       
        pt_order = {
            'MC': "CONTRATACIÓN MÍNIMA CUANTÍA.",
            'SAMC': "SELECCIÓN ABREVIADA DE MENOR CUANTÍA",
            'SI': "SUBASTA INVERSA",
            'LP': "LICITACIÓN PÚBLICA",
            'CM': "CONCURSO DE MÉRITOS",
            'CD': "CONTRATACIÓN DIRECTA",
        }
        
        result = "Unknown"
        if rsc.name in order.values():
            # Find the key for the given name
            result = next(key for key, value in order.items() if value == rsc.name)

        result_pt = "Unknown"
        if pt.name in pt_order.values():
            # Find the key for the given name
            result_pt = next(key for key, value in pt_order.items() if value == pt.name)

        if request.data["acroyms_of_contract"]:
            if pt.name == "CONTRATACIÓN DIRECTA":
                initial_part = f'{result_pt}-{ac.name}-{result}'
            else:
                initial_part = f'{result_pt}-{result}'
        else:
            if pt.name == "CONTRATACIÓN DIRECTA":
                initial_part = f'{result_pt}-{ac.name}-{result}'
            else:
                initial_part = f'{result_pt}-{result}'
        
        automated_number = self.gen_auto(initial_part)
        
        serializer = PlanContratacionMainSerializer(data=request.data)
        if serializer.is_valid():
            # if pt.name == "CONTRATACIÓN DIRECTA":
            #     serializer.validated_data['process_num'] = automated_number
            #     serializer.validated_data['contact_no'] = automated_number
            # else:
            #     serializer.validated_data['process_num'] = automated_number

            serializer.validated_data['state'] = d_state
            serializer.save()
            ActivityTracker.objects.create(
                msg='Se creó un nuevo contrato con NÚMERO DE PROCESO: ' + automated_number,
                action='create',
                sector='hiring',
                user=user
            )
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
    
    def gen_auto(cls, initial_part):
        year = datetime.now().year
        filtered_objects = ContratacionMain.objects.filter(process_num__startswith=initial_part)
        if filtered_objects.exists():
            highest_value = filtered_objects.aggregate(Max('process_num'))['process_num__max']
            print("highest_value", highest_value.split('-')[-1])

            if highest_value is not None:
                # Extract the numeric part from the 'process_num' field
                year_part = int(highest_value.split('-')[-1])
                if year_part >= year:
                    numeric_part = int(highest_value.split('-')[-2])
                    plus_1 = numeric_part + 1
                    count_str = str(plus_1).zfill(3)
                    return f'{initial_part}-{count_str}-{year}'
                else:
                    return f'{initial_part}-001-{year}'
            else:
                return f'{initial_part}-001-{year}'
        else:
            return f'{initial_part}-001-{year}'
        

class get_post_contratacion(APIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = ContratacionMain.objects.all()
        serializerPqrs = ContratacionMainSerializer(queryset, many=True)
        return Response( serializerPqrs.data)
    
    def post(self, request, format=None):
        user = self.request.user
        # process_num = request.data["process_num"]
        pt = processType.objects.get(id=request.data["process"])
        ac = acroymsType.objects.get(id=request.data["acroyms_of_contract"])
        rsc = resSecType.objects.get(id=request.data["responsible_secretary"])

        order = {
            'AMS': "ALCALDÍA MUNICIPAL",
            'SGG': "SECRETARÍA GENERAL Y DE GOBIERNO",
            'SPO': "SECRETARÍA DE PLANEACIÓN Y ORDENAMIENTO TERRITORIAL",
            'SHB': "SECRETARÍA DE HACIENDA Y BIENES",
            'SIE': "SECRETARÍA DE INNOACIÓN Y EMPRENDIMIENTO",
            'SPD': "SECRETARÍA DE PROTECCIÓN SOCIAL Y DESARROLLO COMUNITARIO",
            'SSP': "SECRETARÍA DE SERVICIOS PÚBLICOS Y MEDIO AMBIENTE",
        }

        pt_order = {
            'MC': "CONTRATACIÓN MÍNIMA CUANTÍA.",
            'SAMC': "SELECCIÓN ABREVIADA DE MENOR CUANTÍA",
            'SI': "SUBASTA INVERSA",
            'LP': "LICITACIÓN PÚBLICA",
            'CM': "CONCURSO DE MÉRITOS",
            'CD': "CONTRATACIÓN DIRECTA",
        }
        
        result = "Unknown"
        if rsc.name in order.values():
            # Find the key for the given name
            result = next(key for key, value in order.items() if value == rsc.name)

        result_pt = "Unknown"
        if pt.name in pt_order.values():
            # Find the key for the given name
            result_pt = next(key for key, value in pt_order.items() if value == pt.name)

        if pt.name == "CONTRATACIÓN DIRECTA":
            initial_part = f'{result_pt}-{ac.name}-{result}'
        else:
            initial_part = f'{result_pt}-{result}'
        
        automated_number = self.generate_automated_number(initial_part)
        
        serializer = AllContratacionMainSerializer(data=request.data)
        if serializer.is_valid():
            if pt.name == "CONTRATACIÓN DIRECTA":
                serializer.validated_data['process_num'] = automated_number
                serializer.validated_data['contact_no'] = automated_number
            else:
                serializer.validated_data['process_num'] = automated_number

            serializer.save()
            ActivityTracker.objects.create(
                msg='Se creó un nuevo contrato con NÚMERO DE PROCESO: ' + automated_number,
                action='create',
                sector='hiring',
                user=user
            )
            return Response(serializer.data, status= HTTP_201_CREATED)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
    
    def generate_automated_number(cls, initial_part):
        year = datetime.now().year
        filtered_objects = ContratacionMain.objects.filter(process_num__startswith=initial_part)
        if filtered_objects.exists():
            highest_value = filtered_objects.aggregate(Max('process_num'))['process_num__max']
            print("highest_value", highest_value.split('-')[-1])

            if highest_value is not None:
                # Extract the numeric part from the 'process_num' field
                year_part = int(highest_value.split('-')[-1])
                if year_part >= year:
                    numeric_part = int(highest_value.split('-')[-2])
                    plus_1 = numeric_part + 1
                    count_str = str(plus_1).zfill(3)
                    return f'{initial_part}-{count_str}-{year}'
                else:
                    return f'{initial_part}-001-{year}'
            else:
                return f'{initial_part}-001-{year}'
        else:
            return f'{initial_part}-001-{year}'
        

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'PageSize'
    # max_page_size = 100

class get_contratacion(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = ContratacionMainSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        # queryset = ContratacionMain.objects.all()

        user = self.request.user
        # print("qaws", user.is_organisor)
        if user.is_organisor:
            queryset = ContratacionMain.objects.all()
        elif user.is_consult:
            queryset = ContratacionMain.objects.all()
        elif user.is_hiring_org:
            queryset = ContratacionMain.objects.all()
        elif user.is_hiring and user.username == "43420510":
            queryset = ContratacionMain.objects.all()
        elif user.is_hiring:
            # print("None Org", user.responsible_secretary_id)
            queryset = ContratacionMain.objects.filter(responsible_secretary_id=user.responsible_secretary_id)
        else:
            queryset = None


        # Filter based on request parameters
        state_id = self.request.query_params.get('state_id', None)
        if state_id:
            queryset = queryset.filter(state_id=state_id)
        
        process_id = self.request.query_params.get('process_id', None)
        if process_id:
            queryset = queryset.filter(process_id=process_id)

        process_num = self.request.query_params.get('process_num', None)
        if process_num:
            queryset = queryset.filter(process_num__icontains=process_num)

        process_num_year = self.request.query_params.get('process_num_year', None)
        if process_num_year:
            # Assuming process_num is a CharField
            queryset = queryset.filter(process_num__endswith=process_num_year)

        acroyms_of_contract_id = self.request.query_params.get('acroyms_of_contract_id', None)
        if acroyms_of_contract_id:
            queryset = queryset.filter(acroyms_of_contract_id=acroyms_of_contract_id)
        
        responsible_secretary_id = self.request.query_params.get('responsible_secretary_id', None)
        if responsible_secretary_id:
            queryset = queryset.filter(responsible_secretary_id=responsible_secretary_id)

        contractor_identification = self.request.query_params.get('contractor_identification', None)
        if contractor_identification:
            queryset = queryset.filter(contractor_identification__icontains=contractor_identification)

        contractor = self.request.query_params.get('contractor', None)
        if contractor:
            queryset = queryset.filter(contractor__icontains=contractor)

        contact_no = self.request.query_params.get('contact_no', None)
        if contact_no:
            queryset = queryset.filter(contact_no__icontains=contact_no)
            
        bool_contact_no = self.request.query_params.get('bool_contact_no', None)
        if bool_contact_no:
            queryset = queryset.filter(contact_no__exact='')

        revats = self.request.query_params.get('revats', None)
        if revats:
            queryset = queryset.filter(real_executed_value_according_to_settlement__exact='')
        
        sex = self.request.query_params.get('sex', None)
        if sex:
            queryset = queryset.filter(sex__icontains=sex)
        
        addition = self.request.query_params.get('addition', None)
        if addition:
            queryset = queryset.filter(addition__icontains=addition)

        bpin_project_code_names = self.request.query_params.getlist('bpin_project_code', None)
        if bpin_project_code_names:
            queryset = queryset.filter(bpin_project_code__name__in=bpin_project_code_names)

        typology_id = self.request.query_params.get('typology_id', None)
        if typology_id:
            queryset = queryset.filter(typology_id=typology_id)

        # Filter based on start_date parameter
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(start_date__gte=start_date)
            except ValueError:
                print("Invalid start_date format")

        # Filter based on finish_date parameter
        finish_date = self.request.query_params.get('finish_date', None)
        if finish_date:
            try:
                finish_date = datetime.strptime(finish_date, '%Y-%m-%d').date()
                queryset = queryset.filter(finish_date__lt=finish_date)
            except ValueError:
                print("Invalid start_date format")

         # Check if both start_date and end_date are present
        contract_start_date_str = self.request.query_params.get('contract_start_date_str', None)
        contract_end_date_str = self.request.query_params.get('contract_end_date_str', None)
        if contract_start_date_str and contract_end_date_str:
            try:
                print("***********************contract_start_date_str", contract_start_date_str)
                print("***********************contract_end_date_str", contract_end_date_str)
                start_date = datetime.strptime(contract_start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(contract_end_date_str, '%Y-%m-%d').date()
                queryset = queryset.filter( contract_date__range=[start_date, end_date] )
            except ValueError:
                print("Invalid start_date format")

        return queryset
    

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Count instances where state.name is "EJECUCION"
        ejecucion_count = queryset.filter(state__name="EJECUCION").count()

        # Count instances where state.name is "TERMINADO"
        terminado_count = queryset.filter(state__name="TERMINADO").count()

        # Count instances where state.name is "LIQUIDADO"
        liquidado_count = queryset.filter(state__name="LIQUIDADO").count()

        # Count instances where state.name is "CERRADO"
        cerrado_count = queryset.filter(state__name="CERRADO").count()

        # Count instances of each processType
        process_counts = queryset.values('process__name').annotate(process_count=Count('process'))

        # Count instances of each resSecType
        responsible_secretary_counts = queryset.values('responsible_secretary__name').annotate(responsible_secretary_count=Count('responsible_secretary'))

        # Count instances of each stateType
        state_counts = queryset.values('state__name').annotate(state_count=Count('state'))
       
        # Count instances of each typologyType
        typology_counts = queryset.values('typology__name').annotate(typology_count=Count('typology'))

        # Count instances where sex is "Masculino"
        male_count = queryset.filter(sex="Masculino").count()

        # Count instances where sex is "Femenino"
        female_count = queryset.filter(sex="Femenino").count()

        deactivate_count = queryset.filter(is_active=False).count()
        activate_count = queryset.filter(is_active=True).count()


        # Calculate the accumulated value of contract_value_plus
        accumulated_value = queryset.aggregate(
            total_accumulated_value=Sum(
                Cast('contract_value_plus', output_field=DecimalField(max_digits=15, decimal_places=2))
            )
        )['total_accumulated_value'] or Decimal('0.00')  # Default to 0.00 if no valid values are found
        
        accumulated_valor = queryset.aggregate(
            total_accumulated_value=Sum(
                Cast('worth', output_field=DecimalField(max_digits=15, decimal_places=2))
            )
        )['total_accumulated_value'] or Decimal('0.00') 
         # Default to 0.00 if no valid values are found
        accumulated_revats = queryset.aggregate(
            total_accumulated_value=Sum(
                Cast('real_executed_value_according_to_settlement', output_field=DecimalField(max_digits=15, decimal_places=2))
            )
        )['total_accumulated_value'] or Decimal('0.00')  # Default to 0.00 if no valid values are found

        # accumulated_revats = 0
        # queryset = queryset.order_by('process_num')


        first_initials_order = {
            'C-PS': 1,
            'C-S': 2,
            'C-A': 3,
            'C-INT': 4,
            'C-SL': 5,
            'C-CONS': 6,
            'C-AR': 7,
            'C-OP': 8,
            'C-I': 9,
            'CT-INT': 10,
            'C-T': 11,
            'C-C': 12,
        }

        second_initials_order = {
            'AMS': 1,
            'SGG': 2,
            'SPO': 3,
            'SHB': 4,
            'SIE': 5,
            'SPD': 6,
            'SSP': 7,
        }

        queryset = queryset.annotate(
            first_order=Case(
                *[When(process_num__startswith=key, then=Value(value)) for key, value in first_initials_order.items()],
                default=Value(999), output_field=CharField()
            ),
            second_order=Case(
                *[When(process_num__endswith=key, then=Value(value)) for key, value in second_initials_order.items()],
                default=Value(999), output_field=CharField()
            )
        )

        queryset = queryset.order_by('first_order', 'second_order', 'process_num')


        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = {
                'results': serializer.data,
                'accumulated_value': str(accumulated_value),  # Convert Decimal to string for serialization
                'accumulated_valor': str(accumulated_valor),  # Convert Decimal to string for serialization
                'accumulated_revats': str(accumulated_revats),  # Convert Decimal to string for serialization
                'deactivate_count': deactivate_count,
                'activate_count': activate_count,
                'ejecucion_count': ejecucion_count,
                'terminado_count': terminado_count,
                'liquidado_count': liquidado_count,
                'cerrado_count': cerrado_count,
                'process_counts': process_counts,
                'responsible_secretary_counts': responsible_secretary_counts,
                'state_counts': state_counts,
                'typology_counts': typology_counts,
                'male_count': male_count,
                'female_count': female_count

            }
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'results': serializer.data,
            'accumulated_value': str(accumulated_value),  # Convert Decimal to string for serialization
            'accumulated_valor': str(accumulated_valor),
            'accumulated_revats': str(accumulated_revats),
            'ejecucion_count': ejecucion_count,
            'terminado_count': terminado_count,
            'liquidado_count': liquidado_count,
            'cerrado_count': cerrado_count,
            'process_counts': process_counts,
            'responsible_secretary_counts': responsible_secretary_counts,
            'state_counts': state_counts,
            'typology_counts': typology_counts,
            'male_count': male_count,
            'female_count': female_count
        }

        return Response(response_data)

class ActivateDeactivateContrataction(APIView):
    def post(self, request, pk, *args, **kwargs):
        obj = ContratacionMain.objects.get(id=pk)
        obj.is_active = not obj.is_active
        obj.save()

        action = "activated" if obj.is_active else "deactivated"
        return Response({'message': f'successfully {action}'}, status=status.HTTP_200_OK)
    

class get_filtered_contratacion(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = ContratacionMainSerializer

    def get_queryset(self):
        # queryset = ContratacionMain.objects.all()

        user = self.request.user
        # print("qaws", user.is_organisor)
        if user.is_organisor:
            queryset = ContratacionMain.objects.all()
        elif user.is_consult:
            queryset = ContratacionMain.objects.all()
        elif user.is_hiring_org:
            queryset = ContratacionMain.objects.all()
        elif user.is_hiring and user.username == "43420510":
            queryset = ContratacionMain.objects.all()
        elif user.is_hiring:
            # print("None Org", user.responsible_secretary_id)
            queryset = ContratacionMain.objects.filter(responsible_secretary_id=user.responsible_secretary_id)
        else:
            queryset = None


        # Filter based on request parameters
        state_id = self.request.query_params.get('state_id', None)
        if state_id:
            queryset = queryset.filter(state_id=state_id)
        
        process_id = self.request.query_params.get('process_id', None)
        if process_id:
            queryset = queryset.filter(process_id=process_id)

        process_num = self.request.query_params.get('process_num', None)
        if process_num:
            queryset = queryset.filter(process_num__icontains=process_num)

        acroyms_of_contract_id = self.request.query_params.get('acroyms_of_contract_id', None)
        if acroyms_of_contract_id:
            queryset = queryset.filter(acroyms_of_contract_id=acroyms_of_contract_id)
        
        responsible_secretary_id = self.request.query_params.get('responsible_secretary_id', None)
        if responsible_secretary_id:
            queryset = queryset.filter(responsible_secretary_id=responsible_secretary_id)

        contractor_identification = self.request.query_params.get('contractor_identification', None)
        if contractor_identification:
            queryset = queryset.filter(contractor_identification__icontains=contractor_identification)

        contractor = self.request.query_params.get('contractor', None)
        if contractor:
            queryset = queryset.filter(contractor__icontains=contractor)

        contact_no = self.request.query_params.get('contact_no', None)
        if contact_no:
            queryset = queryset.filter(contact_no__icontains=contact_no)
        
        sex = self.request.query_params.get('sex', None)
        if sex:
            queryset = queryset.filter(sex__icontains=sex)
        
        addition = self.request.query_params.get('addition', None)
        if addition:
            queryset = queryset.filter(addition__icontains=addition)

        bpin_project_code_names = self.request.query_params.getlist('bpin_project_code', None)
        if bpin_project_code_names:
            queryset = queryset.filter(bpin_project_code__name__in=bpin_project_code_names)

        typology_id = self.request.query_params.get('typology_id', None)
        if typology_id:
            queryset = queryset.filter(typology_id=typology_id)

        # Filter based on start_date parameter
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            # Parse the start_date from the request and filter the queryset
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(start_date=start_date)
            except ValueError:
                print("Invalid start_date format")

        # Filter based on finish_date parameter
        finish_date = self.request.query_params.get('finish_date', None)
        if finish_date:
            try:
                finish_date = datetime.strptime(finish_date, '%Y-%m-%d').date()
                queryset = queryset.filter(finish_date__lt=finish_date)
            except ValueError:
                print("Invalid start_date format")

         # Check if both start_date and end_date are present
        contract_start_date_str = self.request.query_params.get('contract_start_date_str', None)
        contract_end_date_str = self.request.query_params.get('contract_end_date_str', None)
        if contract_start_date_str and contract_end_date_str:
            try:
                print("***********************contract_start_date_str", contract_start_date_str)
                print("***********************contract_end_date_str", contract_end_date_str)
                start_date = datetime.strptime(contract_start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(contract_end_date_str, '%Y-%m-%d').date()
                queryset = queryset.filter( contract_date__range=[start_date, end_date] )
            except ValueError:
                print("Invalid start_date format")

        return queryset
    

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Count instances where state.name is "EJECUCION"
        ejecucion_count = queryset.filter(state__name="EJECUCION").count()

        # Count instances where state.name is "EJECUCION"
        terminado_count = queryset.filter(state__name="TERMINADO").count()

        # Count instances of each processType
        process_counts = queryset.values('process__name').annotate(process_count=Count('process'))

        # Count instances of each resSecType
        responsible_secretary_counts = queryset.values('responsible_secretary__name').annotate(responsible_secretary_count=Count('responsible_secretary'))

        # Count instances of each stateType
        state_counts = queryset.values('state__name').annotate(state_count=Count('state'))
       
        # Count instances of each typologyType
        typology_counts = queryset.values('typology__name').annotate(typology_count=Count('typology'))

        # Count instances where sex is "Masculino"
        male_count = queryset.filter(sex="Masculino").count()

        # Count instances where sex is "Femenino"
        female_count = queryset.filter(sex="Femenino").count()

        # Count all
        count = queryset.count()

        # Calculate the accumulated value of contract_value_plus
        accumulated_value = queryset.aggregate(
            total_accumulated_value=Sum(
                Cast('contract_value_plus', output_field=DecimalField(max_digits=15, decimal_places=2))
            )
        )['total_accumulated_value'] or Decimal('0.00')  # Default to 0.00 if no valid values are found

        # queryset = queryset.extra(
        #     select={'contact_no_integer': "substring(contact_no from '\\d+')::integer"},
        #     order_by=['contact_no_integer', 'contact_no']
        # )

        queryset = queryset.order_by('contact_no')

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'results': serializer.data,
            'accumulated_value': str(accumulated_value),  # Convert Decimal to string for serialization
            'ejecucion_count': ejecucion_count,
            'terminado_count': terminado_count,
            'process_counts': process_counts,
            'responsible_secretary_counts': responsible_secretary_counts,
            'state_counts': state_counts,
            'typology_counts': typology_counts,
            'male_count': male_count,
            'female_count': female_count,
            'count': count
        }

        return Response(response_data)


class get_details_contratacion(APIView):
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, pk):
        try:
            return ContratacionMain.objects.get(id=pk)
        except ContratacionMain.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ContratacionById = self.get_object(pk)
        
        serializer = ContratacionMainSerializer(ContratacionById)
        return Response( serializer.data)

    def put(self, request, pk, format=None):
        ContratacionById = self.get_object(pk)
        user = self.request.user
        process_num = request.data["process_num"]
        serializer = AllContratacionMainSerializer(ContratacionById, data=request.data)
        if serializer.is_valid():
            serializer.save()
            ActivityTracker.objects.create(
                msg='Se actualizó un contrato con NÚMERO DE PROCESO: ' + process_num,
                action='update',
                sector='hiring',
                user=user
            )
            return Response(serializer.data)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ContratacionById = self.get_object(pk)
        user = self.request.user
        # ContratacionById.delete()
        ContratacionById.is_deleted = True
        ContratacionById.save()

        ActivityTracker.objects.create(
            msg='Se eliminó un contrato con NÚMERO DE PROCESO:' + ContratacionById.process_num,
            action='delete',
            sector='hiring',
            user=user
        )
        return Response(status= HTTP_204_NO_CONTENT)
    

class NotificationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = self.request.user
        
        order = {
            'AMS': "ALCALDÍA MUNICIPAL",
            'SGG': "SECRETARÍA GENERAL Y DE GOBIERNO",
            'SPO': "SECRETARÍA DE PLANEACIÓN Y ORDENAMIENTO TERRITORIAL",
            'SHB': "SECRETARÍA DE HACIENDA Y BIENES",
            'SIE': "SECRETARÍA DE INNOACIÓN Y EMPRENDIMIENTO",
            'SPD': "SECRETARÍA DE PROTECCIÓN SOCIAL Y DESARROLLO COMUNITARIO",
            'SSP': "SECRETARÍA DE SERVICIOS PÚBLICOS Y MEDIO AMBIENTE",
        }
        
        if user.is_organisor:
            queryset = Notification.objects.all()
        else:
            result = "Unknown"
            if user.responsible_secretary.name in order.values():
                # Find the key for the given name
                result = next(key for key, value in order.items() if value == user.responsible_secretary.name)

            addDash = result+"-"
            queryset = Notification.objects.filter(msg__icontains=addDash)
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListUnusedValueAdded(APIView):
    def get(self, request, format=None):
        # Get all ValueAdded objects that are not linked to any ContratacionMain objects
        unused_value_added = ValueAdded.objects.filter(contratacionmain__isnull=True)

        # Serialize the unused ValueAdded objects
        serializer = ValueAddedSerializer(unused_value_added, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LawFirmView(APIView):
    def get(self, request, pk, format=None):
        objCon = ContratacionMain.objects.get(id=pk)
        objLaw_queryset = LawFirmModel.objects.filter(contract=objCon).order_by("id")

        for objLaw in objLaw_queryset:
            print(objLaw.document)

        serializer = LawFirmSerializer(objLaw_queryset, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        objCon = ContratacionMain.objects.get(id=pk)

        for name in NAMES:
            obj = LawFirmModel(document=name, contract=objCon)
            obj.save()

        return Response("Created Successfully", status=status.HTTP_201_CREATED)
    
    def put(self, request, pk, *args, **kwargs):
        data = request.data
        print("useless, Doing nothing", pk)

        for lawfirm_data in data:
            lawfirm_id = lawfirm_data.get('id')

            lawfirm_instance = LawFirmModel.objects.get(id=lawfirm_id)
            lawfirm_instance.document = lawfirm_data.get('document')
            lawfirm_instance.conservation = lawfirm_data.get('conservation')
            lawfirm_instance.personal_services = lawfirm_data.get('personal_services')
            lawfirm_instance.work_contract = lawfirm_data.get('work_contract')
            lawfirm_instance.direct_contract = lawfirm_data.get('direct_contract')
            lawfirm_instance.fulfills = lawfirm_data.get('fulfills')
            lawfirm_instance.save()

        return Response({'message': 'Data updated successfully'}, status=status.HTTP_200_OK)
    

class UpdateEmptyStateAPIView(APIView):
    def get(self, request, format=None):
        # instances_with_empty_state = ContratacionMain.objects.filter(state__isnull=True, process_num__endswith=2024)
        instances_with_empty_state = ContratacionMain.objects.filter(is_active=False, process_num__endswith=2023)

        for instance in instances_with_empty_state:
            # default_state = StateType.objects.get(id='1')
            instance.is_active = True
            instance.save()

        return Response("Successfully updated for instances", status=status.HTTP_200_OK)