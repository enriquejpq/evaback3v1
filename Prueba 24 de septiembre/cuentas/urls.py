from django.urls import path

from . import views

urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("activar/<uidb64>/<token>/", views.activar, name="activar_cuenta"),
    path("codigo.svg", views.imagen_codigo, name="imagen_codigo"),
]
