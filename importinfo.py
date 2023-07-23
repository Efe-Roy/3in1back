import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import csv
from contratacionAPI.models import ContratacionMain


def cargar_datos_desde_csv(ruta_archivo):
    # Lista para almacenar los registros
    registros = []

    # Abrir el archivo CSV en modo lectura
    with open(ruta_archivo, newline='') as csvfile:
        # Crear un lector CSV
        reader = csv.DictReader(csvfile)

        # Iterar sobre las filas del archivo CSV
        for row in reader:
            # Obtener el valor de acroyms_of_contract del CSV
            acroyms_id = int(row['acroyms_of_contract'])

            # Obtener la instancia del modelo acroymsType según el identificador del CSV
            acroyms_obj = acroymsType.objects.get(id=acroyms_id)

            # Reemplazar el valor del campo 'acroyms_of_contract' con la instancia obtenida
            row['acroyms_of_contract'] = acroyms_obj

            # Agregar cada fila como un registro en la lista de registros
            registros.append(row)

    # Utilizamos list comprehension para crear una lista de objetos ContratacionMain a partir de los registros
    contrataciones = [ContratacionMain(**data) for data in registros]

    # Utilizamos bulk_create para insertar los registros en la base de datos
    ContratacionMain.objects.bulk_create(contrataciones)

# Llamamos al método y proporcionamos la ruta del archivo CSV
ruta_archivo_csv = r"C:\Users\DELL\Documents\contrac.csv"
cargar_datos_desde_csv(ruta_archivo_csv)


