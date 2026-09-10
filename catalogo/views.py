from django.shortcuts import render, get_object_or_404
from .models import Negocio, ProductoServicio, Categoria

def landing(request):
    data_negocio = Negocio.objects.first()
    data_productos = ProductoServicio.objects.filter(stock_activo=True, stock__gt=0)
    
    # 1. 'marca' es texto plano en ProductoServicio: filtramos nulos y vacíos, y ordenamos
    data_marcas = data_productos.exclude(marca__isnull=True).exclude(marca__exact='').values_list('marca', flat=True).distinct().order_by('marca')
    
    # 2. 'categoria_item' es un modelo separado (ForeignKey): 
    # Usamos '__nombre' (o cambia 'nombre' por el campo de texto real de tu modelo Categoria, ej: 'titulo' o 'descripcion')
    data_categorias = data_productos.exclude(categoria_item__isnull=True).values_list('categoria_item__nombre', flat=True).distinct().order_by('categoria_item__nombre')

    contexto = {
        'data_negocio': data_negocio,
        'data_productos': data_productos,
        'data_marcas': data_marcas,
        'data_categorias': data_categorias,
    }
    return render(request, 'landing.html', contexto)




def catalogo_view(request):
  # Capturamos la categoría enviada por URL (ej: /catalogo/?categoria=gaming)
  categoria_seleccionada = request.GET.get('categoria')

  # Capturamos la categoría enviada por URL (ej: /catalogo/?categoria=gaming)
  marca_seleccionada = request.GET.get('marca')

  # Filtramos productos activos
  data_productos = ProductoServicio.objects.filter(stock_activo=True, stock__gt=0)

  # AQUÍ ESTÁ EL CAMBIO CLAVE: filtramos usando el atributo correcto del modelo (categoria_item)
  if categoria_seleccionada:
    data_productos = data_productos.filter(categoria_item=categoria_seleccionada)
  
  if marca_seleccionada:
    data_productos = data_productos.filter(marca=marca_seleccionada)

  data_negocio = Negocio.objects.first()

  contexto = {
      'data_productos': data_productos,
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

def base_views(request, slug):
  # Usamos get_object_or_404 para evitar errores si el slug no existe
  item = get_object_or_404(ProductoServicio, slug=slug)
  data_negocio = Negocio.objects.first()
  contexto = {
      'item': item,
      'data_negocio': data_negocio,
  }
  return render(request, 'base.html', contexto)