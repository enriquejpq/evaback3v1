from django.core.management.base import BaseCommand
from productos.models import Producto
class Command(BaseCommand):
<<<<<<< HEAD
    help="Carga productos de demostración sin duplicarlos (actualiza los existentes)"
    def handle(self,*args,**kwargs):
        datos=[("NutriSalmon Premium","Alimento completo con salmón y vegetales para una vida activa.","alimentos",24990,18,"http://127.0.0.1:8000/static/img/category-food.jpg",True),("Pelota Menta Resistente","Pelota texturizada para juegos seguros, saltos y tardes inolvidables.","juguetes",7990,26,"http://127.0.0.1:8000/static/img/category-toys.jpg",True),("Paseo Coral Set","Collar ajustable y correa reforzada para aventuras con mucho estilo.","accesorios",16990,12,"http://127.0.0.1:8000/static/img/category-accessories.jpg",True)]
        for nombre,descripcion,categoria,precio,stock,imagen,destacado in datos:
            Producto.objects.update_or_create(nombre=nombre,defaults={"descripcion":descripcion,"categoria":categoria,"precio":precio,"stock":stock,"imagen_url":imagen,"destacado":destacado})
=======
    help="Carga productos de demostración sin duplicarlos"
    def handle(self,*args,**kwargs):
        datos=[("NutriSalmon Premium","Alimento completo con salmón y vegetales para una vida activa.","alimentos",24990,18,"/static/img/category-food.jpg",True),("Pelota Menta Resistente","Pelota texturizada para juegos seguros, saltos y tardes inolvidables.","juguetes",7990,26,"/static/img/category-toys.jpg",True),("Paseo Coral Set","Collar ajustable y correa reforzada para aventuras con mucho estilo.","accesorios",16990,12,"/static/img/category-accessories.jpg",True)]
        for nombre,descripcion,categoria,precio,stock,imagen,destacado in datos:
            Producto.objects.get_or_create(nombre=nombre,defaults={"descripcion":descripcion,"categoria":categoria,"precio":precio,"stock":stock,"imagen_url":imagen,"destacado":destacado})
>>>>>>> origin/master
        self.stdout.write(self.style.SUCCESS("Productos de demostración cargados."))
