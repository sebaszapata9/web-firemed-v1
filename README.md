# READme del proyecto

## descripción
La siguiente es una página web catálogo para la empresa FIREMED, que contendrá 50 productos y datos de la empresa que seran renderizados en htmls

### implementación inicial

0. crear repositorio en GitHub
1. abrir carpeta local
2. dentro del cmd colocar: [git init]
3. colocar tambien: [git clone https://github.com/sebaszapata9/web-firemed-v1.git]
4. utilizar carpeta como carpeta de proyecto
5. crear entorno virtual: [python -m venv venv_firemed]
6. activar entorno virtual: [venv_firemed\Scripts\activate.bat]
7. instalar django: [python -m pip install Django]
8. crear proyecto: [django-admin startproject firemed_web .]
9. crear app: [python manage.py startapp catalogo]
10. abrir terminal en VSC
11. activar app en settings


### copiar archivos de demo base

1. app/admin.py
2. app/models.py - tenemos que editar este archivo y adaptar algunas cosas
3. app/urls.py
4. app/views.py

### crear base postgresql

1. instalar psycog: [pip install psycopg2-binary]
2. ingresar a pgadmin y crear base: catalogo_db_firemed
3. configurar base de datos en settings

### correr migración y registrar data de firemed y primeros items

1. instalar Pillow: [python -m pip install Pillow]
2. correr [python manage.py makemigrations]
3. correr [python manage.py migrate]
4. crear super user
5. ingresar a panel admin y crear datos

### copiar templates y validar buen renderizado

1. copiar toda la carpeta templates y static de archivo demo
2. modificar colores del css a colores de marca firemed (#e60000 y #24a803)