from django.urls import path
from . import views
urlpatterns=[path("",views.inicio,name="inicio"),path("catalogo/",views.catalogo,name="catalogo"),path("producto/<int:pk>/",views.detalle_producto,name="detalle_producto"),path("gestion/",views.gestion_productos,name="gestion_productos"),path("gestion/nuevo/",views.crear_producto,name="crear_producto"),path("gestion/<int:pk>/editar/",views.editar_producto,name="editar_producto"),path("gestion/<int:pk>/eliminar/",views.eliminar_producto,name="eliminar_producto")]
