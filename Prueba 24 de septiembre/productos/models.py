from django.core.validators import MinValueValidator
from django.db import models

class Producto(models.Model):
    class Categoria(models.TextChoices):
        ALIMENTOS = "alimentos", "Alimentos"
        JUGUETES = "juguetes", "Juguetes"
        ACCESORIOS = "accesorios", "Accesorios"
        HIGIENE = "higiene", "Higiene y cuidado"
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=600)
    categoria = models.CharField(max_length=20, choices=Categoria.choices, db_index=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(1)])
    stock = models.PositiveIntegerField(default=0)
    imagen_url = models.URLField(max_length=500, blank=True)
    destacado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-destacado", "nombre"]
        verbose_name = "producto"
        verbose_name_plural = "productos"
    def __str__(self): return self.nombre
    @property
    def disponible(self): return self.activo and self.stock > 0
