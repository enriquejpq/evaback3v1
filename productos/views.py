from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductoForm
from .models import Producto

def inicio(request):
    destacados=Producto.objects.filter(activo=True, destacado=True)[:4]
    return render(request,"productos/inicio.html",{"destacados":destacados})

def catalogo(request):
    productos=Producto.objects.filter(activo=True)
    q=request.GET.get("q","").strip()[:100]
    categoria=request.GET.get("categoria","")
    if q: productos=productos.filter(Q(nombre__icontains=q)|Q(descripcion__icontains=q))
    categorias=dict(Producto.Categoria.choices)
    if categoria in categorias: productos=productos.filter(categoria=categoria)
    return render(request,"productos/catalogo.html",{"productos":productos,"q":q,"categoria":categoria,"categorias":Producto.Categoria.choices})

def detalle_producto(request, pk):
    producto=get_object_or_404(Producto,pk=pk,activo=True)
    return render(request,"productos/detalle.html",{"producto":producto})

@login_required
def gestion_productos(request):
    return render(request,"productos/gestion.html",{"productos":Producto.objects.all()})

@login_required
def crear_producto(request):
    form=ProductoForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        producto=form.save(); messages.success(request,f"{producto.nombre} se guardó correctamente en la base de datos."); return redirect("gestion_productos")
    return render(request,"productos/formulario.html",{"form":form,"titulo":"Nuevo producto","accion":"Guardar producto"})

@login_required
def editar_producto(request, pk):
    producto=get_object_or_404(Producto,pk=pk)
    form=ProductoForm(request.POST or None,instance=producto)
    if request.method=="POST" and form.is_valid():
        form.save(); messages.success(request,"Los cambios se guardaron correctamente."); return redirect("gestion_productos")
    return render(request,"productos/formulario.html",{"form":form,"titulo":"Editar producto","accion":"Guardar cambios","producto":producto})

@login_required
def eliminar_producto(request, pk):
    producto=get_object_or_404(Producto,pk=pk)
    if request.method=="POST":
        nombre=producto.nombre; producto.delete(); messages.success(request,f"{nombre} fue eliminado."); return redirect("gestion_productos")
    if request.method!="GET": return HttpResponseNotAllowed(["GET","POST"])
    return render(request,"productos/eliminar.html",{"producto":producto})
