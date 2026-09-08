import pandas as pd
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from catalogo.models import ProductoServicio

class Command(BaseCommand):
    help = 'Carga masiva o actualización de productos desde un archivo Excel a PostgreSQL'

    def add_arguments(self, parser):
        parser.add_argument('ruta_excel', type=str, help='Ruta al archivo Excel')

    def handle(self, *args, **options):
        archivo = options['ruta_excel']
        self.stdout.write(f'Leyendo el archivo {archivo}...')

        try:
            # Leer el archivo Excel usando pandas
            df = pd.read_excel(archivo)
            
            # Reemplazar valores NaN de pandas por None de Python de forma segura
            df = df.where(pd.notnull(df), None)

            contador_procesados = 0
            
            for index, row in df.iterrows():
                # Función auxiliar para limpiar strings que puedan venir como None
                def limpiar(val):
                    if val is None or str(val).strip() == '' or str(val).lower() == 'nan':
                        return ''
                    return str(val).strip()

                nombre = limpiar(row.get('Nombre'))
                sku = limpiar(row.get('SKU'))

                # Omitir filas totalmente vacías o sin SKU
                if not nombre and not sku:
                    continue

                if not sku:
                    self.stdout.write(self.style.WARNING(f"Fila {index + 2}: Omitida por no tener SKU."))
                    continue

                # Generar slug seguro evitando que se corte el SKU
                base_slug = slugify(nombre)
                espacio_para_nombre = 50 - len(str(sku)) - 1
                base_slug_recortado = base_slug[:espacio_para_nombre]
                slug_final = f"{base_slug_recortado}-{sku}" if sku else base_slug[:50]

                # Stock: asegurarnos de que sea numérico o 0 por defecto
                stock_val = row.get('Stock')
                try:
                    stock = int(stock_val) if stock_val is not None and str(stock_val).lower() != 'nan' else 0
                except (ValueError, TypeError):
                    stock = 0

                # Usamos update_or_create buscando por SKU
                ProductoServicio.objects.update_or_create(
                    sku=sku,
                    defaults={
                        'nombre': nombre,
                        'marca': limpiar(row.get('Marca')),
                        'descripcion': limpiar(row.get('Descripción')),
                        'stock': stock,
                        'slug': slug_final
                    }
                )
                contador_procesados += 1

            if contador_procesados > 0:
                self.stdout.write(self.style.SUCCESS(f'¡Se procesaron {contador_procesados} productos exitosamente!'))
            else:
                self.stdout.write(self.style.WARNING('No se encontraron registros válidos para procesar en el Excel.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al procesar el archivo: {e}'))