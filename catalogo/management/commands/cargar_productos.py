import pandas as pd
from django.core.management.base import BaseCommand
from catalogo.models import ProductoServicio  # Reemplaza con tu modelo real

class Command(BaseCommand):
    help = 'Carga masiva de productos desde un archivo Excel a PostgreSQL'

    def add_arguments(self, parser):
        parser.add_argument('ruta_excel', type=str, help='Ruta al archivo Excel')

    def handle(self, *args, **options):
        archivo = options['ruta_excel']
        self.stdout.write(f'Leyendo el archivo {archivo}...')

        try:
            # Leer el archivo Excel usando pandas
            df = pd.read_excel(archivo)
            
            # Opcional: limpiar valores nulos si es necesario
            df = df.where(pd.notnull(df), None)

            productos_a_crear = []
            for _, row in df.iterrows():
                # Mapea las columnas de tu Excel con los campos del modelo
                productos_a_crear.append(
                    ProductoServicio(
                        nombre=row['Nombre'],
                        marca=row['Marca'],
                        descripcion=row['Descripción'],
                        categoria_item=row['Categoría'],  # Asegúrate de que esta columna exista en tu Excel
                        precio=row['Precio'],
                        stock=row['Stock'],
                        sku=row['SKU']
                    )
                )

            # bulk_create inserta todos los objetos en bloque (muy eficiente en PostgreSQL)
            ProductoServicio.objects.bulk_create(productos_a_crear, ignore_conflicts=True)
            
            self.stdout.write(self.style.SUCCESS(f'¡Se cargaron {len(productos_a_crear)} productos exitosamente!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al procesar el archivo: {e}'))