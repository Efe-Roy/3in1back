import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from pqrsAPI.models import EntityType, NameType, MediumResType, StatusType
from contratacionAPI.models import processType, acroymsType, typologyType, resSecType, StateType

EntityData = [
  {"name": "Particular"},
  {"name": "Empleada de la alcaldia"},
  {"name": "Comandante"},
  {"name": "Contratista"},
  {"name": "Hospital San Vicente"},
  {"name": "Secretaria de Despacho"},
  {"name": "Empleado de la alcaldia"},
  {"name": "Inspector 2"},
  {"name": "Inspectora 1"},
  {"name": "Notario"},
  {"name": "Secretario de despacho"},
  {"name": "Colpensiones"},
  {"name": "Concejal"},
  {"name": "Rector Santa Rita"},
  {"name": "Personera"},
  {"name": "Empresa"},
  {"name": "Fiscalia"},
  {"name": "Gobernacion"},
  {"name": "concejales"},
  {"name": "Alcalde"},
  {"name": "Fiscal"},
  {"name": "Concejo"},
  {"name": "Patrullero"},
  {"name": "Rector La Magdalena"},
  {"name": "Sanidad"},
  {"name": "Centro de Bienestar del Anciano"},
  {"name": "Comunidad"},
  {"name": "Dane"},
  {"name": "Gerente Hospital"},
  {"name": "Registrador"},
  {"name": "secretario de Despacuo"},
  {"name": "Abogado"},
  {"name": "Abogado del sindicato"},
  {"name": "Abogado Sindicato"},
  {"name": "Acueducto"},
  {"name": "Acueducto la enea"},
  {"name": "anulado el radicado por error de digitacion no fue utilizado"},
  {"name": "Asociacion"},
  {"name": "CDI"},
  {"name": "Consorcio Omega"},
  {"name": "Contraloria"},
  {"name": "Contratista Obra"},
  {"name": "Contratita"},
  {"name": "Coordinadora CDI"},
  {"name": "coredi"},
  {"name": "Diputado"},
  {"name": "Docentes"},
  {"name": "EPM"},
  {"name": "Ferreteria"},
  {"name": "Fundacion"},
  {"name": "J.A.C"},
  {"name": "Jefe de Oficina"},
  {"name": "Mayor del Ejercito"},
  {"name": "Particulares"},
  {"name": "Presidente J.A.C"},
  {"name": "Procuraduria"},
  {"name": "Prosperidad Social"},
  {"name": "Provincia"},
  {"name": "Rector Piedra Gorda"},
  {"name": "Representante del Sindicato"},
  {"name": "Reverenda"},
  {"name": "Secretario de Planeación"},
  {"name": "Sindicato"},
  {"name": "Sociedad de Mejoras Publicas"},
  {"name": "Veeduria Ciudadana"}
]

NameData = [
  { "name": "Solicitud" },
  { "name": "Informe" },
  { "name": "Propuesta" },
  { "name": "Derecho de Peticion" },
  { "name": "Querella" },
  { "name": "Invitacion" },
  { "name": "Queja" },
  { "name": "Respueta" },
  { "name": "Peticion" },
  { "name": "Apelacion" },
  { "name": "Denuncia" },
  { "name": "informacion" },
  { "name": "accion preventiva" },
  { "name": "anulado el radicado por error de digitacion no fue utilizado" },
  { "name": "Notificacion" },
  { "name": "renuncia" },
  { "name": "Rescurso de apelacion" }
]

ProcessData = [
  { "name": "LICITACIÓN PÚBLICA" },
  { "name": "SELECCIÓN ABREVIADA. (DE MENOR CUANTÍA, SUBASTA)" },
  { "name": "CONCURSO DE MÉRITOS" },
  { "name": "CONTRATACIÓN DIRECTA" },
  { "name": "CONTRATACIÓN MÍNIMA CUANTÍA." }
]

acroymsData = [
  { "name": "C-PS" },
  { "name": "C-S" },
  { "name": "C-A" },
  { "name": "C-INT" },
  { "name": "C-SL" },
  { "name": "C-CONS" },
  { "name": "C-AR" },
  { "name": "C-OP" },
  { "name": "C-I" },
  { "name": "CT-INT" },
  { "name": "C-T" },
  { "name": "C-C" },
  { "name": "C-AP" },
  { "name": "C-CP" }
]

typologyData = [
  { "name": "PRESTACIÓN DE SERVICIOS" },
  { "name": "SUMINISTRO" },
  { "name": "CONVENIO DE ASOCIACIÓN" },
  { "name": "CONVENIO INTERADMINISTRATIVO" },
  { "name": "CONVENIO SOLIDARIO" },
  { "name": "CONSULTORÍA" },
  { "name": "ARRENDAMIENTO" },
  { "name": "OBRA PÚBLICA" },
  { "name": "INTERVENTORÍA" },
  { "name": "CONTRATO INTERADMINISTRATIVO" },
  { "name": "CONTRATO DE TRABAJO" },
  { "name": "CONTRATO DE APRENDIZAJE" },
  { "name": "CONVENIO DE PRACTICA" }
]

resSecData = [
  { "name": "ALCALDÍA MUNICIPAL" },
  { "name": "SECRETARÍA GENERAL Y DE GOBIERNO" },
  { "name": "SECRETARÍA DE PLANEACIÓN Y ORDENAMIENTO TERRITORIAL" },
  { "name": "SECRETARÍA DE HACIENDA Y BIENES" },
  { "name": "SECRETARÍA DE INNOACIÓN Y EMPRENDIMIENTO" },
  { "name": "SECRETARÍA DE PROTECCIÓN SOCIAL Y DESARROLLO COMUNITARIO" },
  { "name": "SECRETARÍA DE SERVICIOS PÚBLICOS Y MEDIO AMBIENTE" }
]

stateData = [
  { "name": "EJECUCION" },
  { "name": "TERMINADO" },
  { "name": "LIQUIDADO" },
  { "name": "CERRADO" }
]

mediumResData = [
  {"name": "(Blanks)"},
  {"name": "Oficio"},
  {"name": "Reparto"},
  {"name": "comité"},
  {"name": "Correo"},
  {"name": "PERMISO"},
  {"name": "Resolucion"},
  {"name": "se inicio proceso caso reservado proteccion de menor"},
  {"name": "Entrega fisica de resolucion"},
  {"name": "Reaprto"},
  {"name": "Autorizacion"},
  {"name": "COMITÉ ESPASIO PUBLICO"},
  {"name": "No se autorizo el permiso, no realizo el pago del espacio solicitado"},
  {"name": "prestamo verbal"},
  {"name": "Radicado Anulado"},
  {"name": "Se remite al comité de consejo de seguridad"},
  {"name": "Acta"},
  {"name": "Acta de comité de convivencia"},
  {"name": "Acta de liquidacion"},
  {"name": "Anulada por el remitente, reclamo la solicitud presentada"},
  {"name": "anulado el radicado por error de digitacion no fue utilizado"},
  {"name": "Canceló el comparendo"},
  {"name": "comité de victimas"},
  {"name": "contratista rodolfo"},
  {"name": "contratsita rodolfo"},
  {"name": "decreto"},
  {"name": "Decreto 124"},
  {"name": "Decreto 129"},
  {"name": "el abogado no recibe la carpeta"},
  {"name": "El remitente reclama el oficio Radicado."},
  {"name": "El remitente retira la solicitud"},
  {"name": "EL SECRETARIO DE HACIENDA NO RECIBIO EL OFICIO Y POR ENDE NO TIENE FIRMA DE RECIBIDO"},
  {"name": "inicia proceso por alto volumen de la musica varios establecimientos"},
  {"name": "NO APLICA"},
  {"name": "no se autorizo, el señor cambio la fecha de la solicitud"},
  {"name": "no se dio respuesta por escrito, pero se realizo acompañamiento por la fuerza publica los diasd solicitados."},
  {"name": "Radicado anulado, el remitente reclamo la solicitud"},
  {"name": "radicado no se utilizo"},
  {"name": "Resolucio 261"},
  {"name": "Resolucion 043"},
  {"name": "Resolucion 239"},
  {"name": "Resolucion 272"},
  {"name": "Resolucion 273"},
  {"name": "Resolucion 295"},
  {"name": "Resolucion 297"},
  {"name": "Resolucion 300"},
  {"name": "Resolucion 301"},
  {"name": "Resolucion 321"},
  {"name": "Resolucion 349"},
  {"name": "Resolucion 393"},
  {"name": "Resolucion 394"},
  {"name": "RESOLUCION 418 30/12/2022"},
  {"name": "RESOLUCION 419 30/12/2022"},
  {"name": "retiro solicitud"},
  {"name": "reunion comité de discapacidad"},
  {"name": "se anexo a proceso"},
  {"name": "Se anula el radicado, la informacion solicitada es para san Vicnete del Caguan."},
  {"name": "se anulo el radicado, el remitente reclamo la solicitud"},
  {"name": "se autorizo el permiso pero el solicitante no acepto el horario"},
  {"name": "Se devuelve el docuemento por que se encontrava incompleto"},
  {"name": "Se devuelve el radicado por competencia del muncipio de Guarne"},
  {"name": "Se dio respuesta, por medio de oficio o memorial"},
  {"name": "Se Envia Oficio a la entidad D1"},
  {"name": "se incio proceso, caso reservado"},
  {"name": "se inicioa proceso de minima cuantia"},
  {"name": "se realizo acompaamiento por parte de la comisaria el dia solicitado."},
  {"name": "se realizo reporte con la contadora, pagina chip local."},
  {"name": "Se realizo reunion con el cetro de bienestar y se programo para el 10 de diciembre de 2022"},
  {"name": "Se remite a masora por competencia"},
  {"name": "Se remite a personeria por competencia"},
  {"name": "Se remite a planeacion para seunda instancia"},
  {"name": "se remitio a la comision nacional"},
  {"name": "se Soicio proceso radicado emservado proteccion presunto menor"},
  {"name": "SEGUNDA INSTANCIA"},
  {"name": "Transporte"},
  {"name": "verbal reunion con presidente de santa ana"},
  {"name": "viaticos"}
]

StatusData = [
    {"name": "In Progress"},
    {"name": "Expire Soon"},
    {"name": "Completed"}
]

for item in EntityData:

    EntityType.objects.create(
        name=item['name']
    )
    print("EntityType completed")

for item in NameData:

    NameType.objects.create(
        name=item['name']
    )
    print("NameType completed")

for item in mediumResData:

    MediumResType.objects.create(
        name=item['name']
    )
    print("MediumResType completed")

for item in StatusData:

    StatusType.objects.create(
        name=item['name']
    )
    print("StatusType completed")


# ===================================  ======================================
# ===================================  ======================================

for item in ProcessData:

    processType.objects.create(
        name=item['name']
    )
    print("processType completed")

for item in acroymsData:

    acroymsType.objects.create(
        name=item['name']
    )
    print("acroymsType completed")

for item in typologyData:

    typologyType.objects.create(
        name=item['name']
    )
    print("typologyType completed")

for item in resSecData:

    resSecType.objects.create(
        name=item['name']
    )
    print("resSecType completed")

for item in stateData:

    StateType.objects.create(
        name=item['name']
    )
    print("StateType completed")



