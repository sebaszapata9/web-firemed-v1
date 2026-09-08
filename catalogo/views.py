from django.shortcuts import render, get_object_or_404
from .models import Negocio, ProductoServicio, Category

def landing(request):
  data_negocio = Negocio.objects.first()
  productos = ProductoServicio.objects.filter(stock_activo=True, stock__gt=0)
  contexto = {
      'data_negocio': data_negocio,
      'items': productos,
  }
  return render(request, 'landing.html', contexto)




def lista_items(request):
  # Capturamos la categoría enviada por URL (ej: /catalogo/?categoria=gaming)
  categoria_seleccionada = request.GET.get('categoria')

  # Filtramos productos activos
  productos = ProductoServicio.objects.filter(stock_activo=True, stock__gt=0)

  # AQUÍ ESTÁ EL CAMBIO CLAVE: filtramos usando el atributo correcto del modelo (categoria_item)
  if categoria_seleccionada:
    productos = productos.filter(categoria_item=categoria_seleccionada)

  data_negocio = Negocio.objects.first()

  contexto = {
      'items': productos,
      'data_negocio': data_negocio,
      'categoria_actual': categoria_seleccionada,
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