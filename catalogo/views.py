from django.shortcuts import render, get_object_or_404
from .models import Negocio, ProductoServicio, Category

def landing(request):
    data_negocio = Negocio.objects.first()
    productos = ProductoServicio.objects.filter(stock_activo=True, stock__gt=0)
    
    # 1. 'marca' es texto plano en ProductoServicio: filtramos nulos y vacíos, y ordenamos
    data_marcas = productos.exclude(marca__isnull=True).exclude(marca__exact='').values_list('marca', flat=True).distinct().order_by('marca')
    
    # 2. 'categoria_item' es un modelo separado (ForeignKey): 
    # Usamos '__nombre' (o cambia 'nombre' por el campo de texto real de tu modelo Category, ej: 'titulo' o 'descripcion')
    data_categorias = productos.exclude(categoria_item__isnull=True).values_list('categoria_item__name', flat=True).distinct().order_by('categoria_item__name')

    contexto = {
        'data_negocio': data_negocio,
        'items': productos,
        'data_marcas': data_marcas,
        'data_categorias': data_categorias,
    }
    return render(request, 'landing.html', contexto)




def lista_items(request):
  # Capturamos la categoría enviada por URL (ej: /catalogo/?categoria=gaming)
  categoria_seleccionada = request.GET.get('categoria')

  # Capturamos la categoría enviada por URL (ej: /catalogo/?categoria=gaming)
  marca_seleccionada = request.GET.get('marca')

  # Filtramos productos activos
  productos = ProductoServicio.objects.filter(stock_activo=True, stock__gt=0)

  # AQUÍ ESTÁ EL CAMBIO CLAVE: filtramos usando el atributo correcto del modelo (categoria_item)
  if categoria_seleccionada:
    productos = productos.filter(categoria_item=categoria_seleccionada)
  
  if marca_seleccionada:
    productos = productos.filter(marca=marca_seleccionada)

  data_negocio = Negocio.objects.first()

  contexto = {
      'items': productos,
      'data_negocio': data_negocio,
      'categoria_actual': categoria_seleccionada,
      'marca_actual': marca_seleccionada,
  }

  # Renderizado directo con el nombre de template exacto
  return render(request, 'catalogo.html', contexto)



def detalle_item(request, slug):
  # Usamos get_object_or_404 para evitar errores si el slug no existe
  item = get_object_or_404(ProductoServicio, slug=slug)
  data_negocio = Negocio.objects.first()
  contexto = {
      'item': item,
      'data_negocio': data_negocio,
  }
  return render(request, 'item.html', contexto)