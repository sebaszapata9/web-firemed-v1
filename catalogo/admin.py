from django.contrib import admin
from .models import Categoria, ProductoServicio, Negocio

# Register your models here.

class ProductoServicioAdmin(admin.ModelAdmin):
  list_display = ("nombre", "marca", "precio", "stock","sku")
  search_fields = ('nombre', 'marca')
  list_filter = ('stock_activo', 'marca')
  prepopulated_fields = {'slug': ('nombre',)}  # Autocompletar el slug
  
admin.site.register(ProductoServicio, ProductoServicioAdmin)

class NegocioAdmin(admin.ModelAdmin):
  list_display = ("nombre", "telefono", "correo_electronico")
  
admin.site.register(Negocio, NegocioAdmin)

class CategoriaAdmin(admin.ModelAdmin):
  list_display = ("nombre", "slug")
  
admin.site.register(Categoria, CategoriaAdmin)