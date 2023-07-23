import json
from django.core.management.base import BaseCommand
from contratacionAPI.models import ContratacionMain

class Command(BaseCommand):
    help = 'Seed data into the ContratacionMain model from JSON file'

    def handle(self, *args, **kwargs):
        with open('pqrs/AMS-ALCALDIA.json') as f:
            data = json.load(f)

        for item in data:
            contrato = ContratacionMain.objects.create(
                proceso=item["PROCESO"],
                tipologia=item["TIPOLOGIA"],
                numero_contrato=item["No. DEL CONTRATO"],
                contratista=item["CONTRATISTA"],
                identificacion_contratista=item["IDENTIFICACION CONTRATISTA"],
                digito_verificacion_rut_o_nit=item["DIGITO DE VERIFICACIÓN RUT O NIT"],
                fecha_nacimiento=item["FECHA DE NACIMIENTO"],
                tipo_sangre=item["Tipo de Sangre (RH)"],
                sexo=item["SEXO"],
                objeto=item["OBJETO"],
                valor=item["VALOR "],
                duracion=item["DURACIÓN"],
                fecha_contrato=item["FECHA CONTRATO"],
                fecha_inicio=item["FECHA INICIO"],
                fecha_terminacion=item["FECHA DE TERMINACIÓN"],
                anticipo=item["ANTICIPO"],
                reporte_proceso_secop_inicio=item["REPORTE DEL PROCESO EN EL SECOP CUANDO INICIA"],
                reporte_secop_contrato=item["REPORTE SECOP DEL CONTRATO"],
                reporte_antioquia_honesta=item["REPORTE EN ANTIOQUIA HONESTA"],
                reporte_web_institucional=item["REPORTE EN WEB INSTITUCIONAL"],
                reporte_gestiontransparente=item["REPORTE GESTIONTRANSPARENTE.COM"],
                acta_liquidacion=None if item["ACTA DE LIQUIDACIÓN"] == "null" else item["ACTA DE LIQUIDACIÓN"],
                reporte_liquidacion=None if item["REPORTE LIQUIDACIÓN"] == "null" else item["REPORTE LIQUIDACIÓN"],
                fecha_acta_cierre_reporte=None if item["FECHA ACTA DE CIERRE Y FECHA REPORTE"] == "null" else item["FECHA ACTA DE CIERRE Y FECHA REPORTE"],
                adicion=item["ADICION"],
                valor_adicion=None if item["VALOR ADICION"] == "null" else item["VALOR ADICION"],
                tiempo_adicion=None if item["TIEMPO ADICION"] == "null" else item["TIEMPO ADICION"],
                codigo_proyecto_bpin=item["CÓDIGO DEL PROYECTO BPIN"],
                valor_afectado_proyecto_bpin_cdp=item["VALOR AFECTADO POR PROYECTO BPIN EN CDP"],
                articulos_presupuestales=item["ARTÍCULOS PRESUPUESTALES"],
                denominacion_rubro=item["DENOMINACIÓN DEL RUBRO"],
                valor_rubro=item["VALOR DEL RUBRO"],
                estado=item["ESTADO"],
                secretaria_responsable=item["SECRETARIA RESPONSABLE"],
                supervisor_contrato_interventor=item["NOMBRE DEL SUPERVISOR DEL CONTRATO Y/O INTERVENTOR"],
                observaciones=item["OBSERVACIOES"],
                valor_contrato_mas_adiciones=item["VALOR CONTRATO MÁS LAS ADICIONES"],
                valor_real_ejecutado_liquidacion=None if item["VALOR REAL EJECUTADO SEGÚN ACTA DE LIQUIDACIÓN"] == "null" else item["VALOR REAL EJECUTADO SEGÚN ACTA DE LIQUIDACIÓN"],
                estado_archivo=item["ESTADO ARCHIVO"],
            )
            contrato.save()

        self.stdout.write(self.style.SUCCESS('Data seeding completed!'))
