from django.shortcuts import render, get_object_or_404
from .models import Negocio, ProductoServicio, Categoria


def landing(request):
    data_negocio = Negocio.objects.first()
    data_productos = ProductoServicio.objects.filter(stock_activo=True, stock__gt=0)

    data_marcas = (
        data_productos
        .exclude(marca__isnull=True)
        .exclude(marca__exact='')
        .values_list('marca', flat=True)
        .distinct()
        .order_by('marca')
    )

    data_categorias = (
        data_productos
        .exclude(categoria_item__isnull=True)
        .values_list('categoria_item__nombre', flat=True)
        .distinct()
        .order_by('categoria_item__nombre')
    )

    contexto = {
        'data_negocio': data_negocio,
        'data_productos': data_productos,
        'data_marcas': data_marcas,
        'data_categorias': data_categorias,
    }
    return render(request, 'landing.html', contexto)


def catalogo_view(request):
    categoria_seleccionada = request.GET.get('categoria', '').strip()
    marca_seleccionada = request.GET.get('marca', '').strip()
    busqueda = request.GET.get('q', '').strip()

    data_productos = (
        ProductoServicio.objects
        .filter(stock_activo=True, stock__gt=0)
        .select_related('categoria_item')
        .order_by('nombre')
    )

    if categoria_seleccionada:
        data_productos = data_productos.filter(categoria_item__slug=categoria_seleccionada)

    if marca_seleccionada:
        data_productos = data_productos.filter(marca=marca_seleccionada)

    if busqueda:
        data_productos = data_productos.filter(
            nombre__icontains=busqueda
        ) | data_productos.filter(
            marca__icontains=busqueda
        ) | data_productos.filter(
            sku__icontains=busqueda
        )

    categorias = (
        Categoria.objects
        .filter(productoservicio__stock_activo=True, productoservicio__stock__gt=0)
        .distinct()
        .order_by('nombre')
    )

    marcas = (
        ProductoServicio.objects
        .filter(stock_activo=True, stock__gt=0)
        .exclude(marca__isnull=True)
        .exclude(marca__exact='')
        .values_list('marca', flat=True)
        .distinct()
        .order_by('marca')
    )

    data_negocio = Negocio.objects.first()

    contexto = {
        'data_productos': data_productos.distinct(),
        'data_negocio': data_negocio,
        'categorias': categorias,
        'marcas': marcas,
        'categoria_actual': categoria_seleccionada,
        'marca_actual': marca_seleccionada,
        'busqueda_actual': busqueda,
    }

    return render(request, 'catalogo.html', contexto)


def detalle_item(request, slug):
    item = get_object_or_404(
        ProductoServicio.objects.select_related('categoria_item'),
        slug=slug,
        stock_activo=True,
    )
    data_negocio = Negocio.objects.first()

    productos_relacionados = (
        ProductoServicio.objects
        .filter(
            stock_activo=True,
            stock__gt=0,
            categoria_item=item.categoria_item,
        )
        .exclude(pk=item.pk)
        .order_by('nombre')[:4]
    )

    contexto = {
        'item': item,
        'data_negocio': data_negocio,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'item.html', contexto)
