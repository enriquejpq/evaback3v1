from django import forms
from django.core.exceptions import ValidationError
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model=Producto
        fields=["nombre","descripcion","categoria","precio","stock","imagen_url","destacado","activo"]
        labels={"imagen_url":"Enlace de la imagen"}
        widgets={"descripcion":forms.Textarea(attrs={"rows":4,"maxlength":600}),"precio":forms.NumberInput(attrs={"min":1,"step":1}),"stock":forms.NumberInput(attrs={"min":0}),"imagen_url":forms.URLInput(attrs={"placeholder":"https://ejemplo.cl/imagen.jpg"})}
    def clean_nombre(self):
        nombre=" ".join(self.cleaned_data["nombre"].split())
        if len(nombre)<3: raise ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre
    def clean_descripcion(self):
        texto=self.cleaned_data["descripcion"].strip()
        if len(texto)<15: raise ValidationError("Describe el producto con al menos 15 caracteres.")
        return texto
