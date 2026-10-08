from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .forms import ProductoForm
from .models import Producto
class TiendaTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(username="equipo",password="ClaveSegura2026!")
        self.producto=Producto.objects.create(nombre="Snack natural",descripcion="Snack saludable para perros adultos.",categoria="alimentos",precio=4990,stock=8)
    def test_catalogo_publico(self): self.assertContains(self.client.get(reverse("catalogo")),"Snack natural")
    def test_gestion_requiere_login(self): self.assertRedirects(self.client.get(reverse("gestion_productos")),f"{reverse('login')}?next={reverse('gestion_productos')}")
    def test_usuario_autenticado_crea_producto(self):
        self.client.login(username="equipo",password="ClaveSegura2026!")
        r=self.client.post(reverse("crear_producto"),{"nombre":"Arnés seguro","descripcion":"Arnés acolchado para paseos cómodos y seguros.","categoria":"accesorios","precio":12990,"stock":5,"imagen_url":"","activo":"on"})
        self.assertRedirects(r,reverse("gestion_productos")); self.assertTrue(Producto.objects.filter(nombre="Arnés seguro").exists())
    def test_validacion_impide_descripcion_corta(self):
        form=ProductoForm({"nombre":"Arnés","descripcion":"corta","categoria":"accesorios","precio":1000,"stock":1,"activo":True})
        self.assertFalse(form.is_valid()); self.assertIn("descripcion",form.errors)
    def test_eliminar_solo_con_post(self):
        self.client.login(username="equipo",password="ClaveSegura2026!")
        self.client.get(reverse("eliminar_producto",args=[self.producto.pk])); self.assertTrue(Producto.objects.filter(pk=self.producto.pk).exists())
