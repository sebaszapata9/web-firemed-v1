from email.utils import quote

from django.db import models

# Create your models here.



# 1. Modelo independiente para las categorías (Administrable desde el Django Admin)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categorías"


# 2. Modelo para la empresa o negocio que ofrece los productos o servicios
class Negocio(models.Model):
	nombre = models.CharField(max_length=255)
	descripcion = models.TextField()
	direccion = models.CharField(max_length=255)
	telefono = models.CharField(max_length=20, verbose_name="Teléfono de contacto (colocar con código de país, ej: 51987654321)")
	correo_electronico = models.EmailField()
	logo = models.ImageField(upload_to='logos/', blank=True, null=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)



# 3. Modelo para los productos o servicios ofrecidos por el negocio  
class ProductoServicio(models.Model):
	nombre = models.CharField(max_length=255)
	marca = models.CharField(max_length=255)
	descripcion = models.TextField()
	imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)
	categoria_prod_servicio = models.CharField(max_length=255, choices=[
		('producto', 'Producto'),
		('servicio', 'Servicio')], blank=True, null=True)
	categoria_item = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT,  # Evita que borren una categoría si tiene productos activos
        verbose_name="Categoría", null=True, blank=True
    )
	precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	slug = models.SlugField(max_length=255, unique=True, auto_created=True, verbose_name="Slug URL (se llena en automático)")
	stock = models.PositiveIntegerField()
	sku = models.CharField(max_length=100, unique=True, verbose_name="SKU (Código de Producto)", blank=True, null=True)
	ficha_tecnica = models.FileField(upload_to='fichas_tecnicas/', blank=True, null=True)
	stock_activo = models.BooleanField(default=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.nombre} - {self.categoria_item}"
