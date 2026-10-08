from django.db import migrations, models
import django.core.validators
class Migration(migrations.Migration):
    initial=True
    dependencies=[]
    operations=[migrations.CreateModel(name="Producto",fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("nombre",models.CharField(max_length=100,unique=True)),("descripcion",models.TextField(max_length=600)),("categoria",models.CharField(choices=[("alimentos","Alimentos"),("juguetes","Juguetes"),("accesorios","Accesorios"),("higiene","Higiene y cuidado")],db_index=True,max_length=20)),("precio",models.DecimalField(decimal_places=0,max_digits=10,validators=[django.core.validators.MinValueValidator(1)])),("stock",models.PositiveIntegerField(default=0)),("imagen_url",models.URLField(blank=True,max_length=500)),("destacado",models.BooleanField(default=False)),("activo",models.BooleanField(default=True)),("creado",models.DateTimeField(auto_now_add=True)),("actualizado",models.DateTimeField(auto_now=True))],options={"verbose_name":"producto","verbose_name_plural":"productos","ordering":["-destacado","nombre"]})]
