from django.contrib import admin
from django.urls import include, path
<<<<<<< HEAD
urlpatterns = [path("admin/", admin.site.urls), path("cuenta/", include("cuentas.urls")), path("cuenta/", include("django.contrib.auth.urls")), path("", include("productos.urls"))]
=======
urlpatterns = [path("admin/", admin.site.urls), path("cuenta/", include("django.contrib.auth.urls")), path("", include("productos.urls"))]
>>>>>>> origin/master
