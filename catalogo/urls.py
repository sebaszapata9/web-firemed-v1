from django.urls import path
from . import views

urlpatterns = [
    path('catalogo/', views.lista_items, name='lista_items'),
    path('', views.landing, name='landing'),
    path('catalogo/<slug:slug>/', views.detalle_item, name='detalle_item')
    ]


"""Este urls.py es específico para la aplicación que hemos creado. 
Tenemos que hacer la conexión el directorio raíz de la aplicación creada, 
en este caso app_name.

Hay un archivo llamado urls.py en el directorio del proyecto proyecto_1, 
dentro del archivo tenemos que agregar el módulo include dentro de la declaración import

Tambien tenemos que agregar la función path dentro de la lista urlpatterns[ ], 
con argumentos que van a enrutar a los usuarios al visitar la aplicación web.
"""